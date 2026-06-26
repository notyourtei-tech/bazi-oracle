from flask import Flask, render_template, request, redirect, session, Response, jsonify, send_file, abort
from flask_migrate import Migrate
from functools import wraps
from dotenv import load_dotenv
import json
import io
import os
import re
import secrets
import logging
import gzip
from datetime import timedelta

from config import Config, _get_secret_key

from models.user import db, User
from models.chart import Chart

from core.pipeline import run_full_analysis_from_birth
from core.cache import bazi_cache
from core.ai_engine import generate_ai_analysis, generate_ai_analysis_stream
from core.share_card import generate_share_card, HAS_PILLOW
from core.daily_fortune_engine import calc_daily_fortune, calc_weekly_fortune, calc_monthly_fortune
from core.compatibility_engine import analyze_compatibility
from core.pdf_engine import generate_pdf_report, HAS_REPORTLAB
from core.comprehensive_analysis import analyze_dayun_comprehensive, analyze_liunian_comprehensive, STEM_ELEMENT
from core.security import (
    generate_csrf_token, csrf_protect, check_rate_limit,
    check_login_rate_limit, record_login_attempt, reset_login_attempts,
    validate_birth_date, validate_birth_time, validate_name, validate_city,
    validate_csrf_token, safe_error_response, VALID_COUNTRIES, VALID_GENDERS,
    register_temp_file, validate_result_dict, check_user_api_rate_limit
)

# ========================
# 日志配置
# ========================
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# ========================
# Flask App
# ========================
load_dotenv()
app = Flask(__name__)

# 密钥：优先环境变量，否则持久化到文件（重启不会丢失）
app.secret_key = _get_secret_key()

# 数据库
app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = Config.SQLALCHEMY_ENGINE_OPTIONS
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Session 安全
app.config["SESSION_COOKIE_HTTPONLY"] = Config.SESSION_COOKIE_HTTPONLY
app.config["SESSION_COOKIE_SAMESITE"] = Config.SESSION_COOKIE_SAMESITE
app.config["SESSION_COOKIE_SECURE"] = Config.SESSION_COOKIE_SECURE
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)

# 上传限制
app.config["MAX_CONTENT_LENGTH"] = Config.MAX_CONTENT_LENGTH

db.init_app(app)
migrate = Migrate(app, db)

# 模板中可用 csrf_token
app.jinja_env.globals['csrf_token'] = generate_csrf_token


# ========================
# 安全中间件
# ========================

@app.before_request
def security_checks():
    """请求前安全检查"""
    # 限流
    if not check_rate_limit():
        return safe_error_response("error_rate_limit", 429)

    # API 端点 CSRF 验证（公开只读 API 无需 CSRF）
    _csrf_exempt_paths = {
        '/api/share-card', '/api/daily-fortune', '/api/weekly-fortune',
        '/api/monthly-fortune', '/api/compatibility', '/api/export-pdf',
    }
    if request.path.startswith('/api/') and request.method in ('POST', 'PUT', 'DELETE', 'PATCH'):
        if request.path not in _csrf_exempt_paths:
            validate_csrf_token()

    # 阻止常见攻击路径
    blocked_paths = [
        '/wp-admin', '/phpmyadmin', '/.env', '/config', '/backup',
        '/.git', '/.svn', '/.htaccess', '/wp-login', '/xmlrpc.php',
        '/wp-content', '/wp-includes', '/administrator', '/admin',
        '/cgi-bin', '/scripts', '/phpinfo', '/server-status'
    ]
    path_lower = request.path.lower()
    for path in blocked_paths:
        if path_lower.startswith(path):
            abort(404)

    # 阻止路径穿越攻击
    if '..' in request.path or '%2e%2e' in request.path.lower():
        abort(404)

    # 阻止 null 字节注入
    if '\x00' in request.path or '%00' in request.path:
        abort(404)


@app.after_request
def security_headers(response):
    """添加安全响应头"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), camera=(), microphone=()'
    response.headers['X-Permitted-Cross-Domain-Policies'] = 'none'

    # 静态资源长期缓存
    if request.path.startswith('/static/'):
        response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
    elif request.path.endswith('.html') or request.path == '/' or request.path == '':
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'

    # HSTS（仅在HTTPS环境下有意义）
    if request.is_secure or os.environ.get('FORCE_HTTPS'):
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'

    # CSP
    csp_parts = [
        "default-src 'self'",
        "script-src 'self' 'unsafe-inline'",
        "style-src 'self' 'unsafe-inline'",
        "img-src 'self' data:",
        "font-src 'self'",
        "connect-src 'self'",
        "frame-ancestors 'none'",
        "base-uri 'self'",
        "form-action 'self'"
    ]
    response.headers['Content-Security-Policy'] = "; ".join(csp_parts)

    return response


@app.after_request
def compress_response(response):
    """Gzip压缩响应体"""
    # Skip SSE streaming responses — they must stream incrementally
    if response.content_type and 'text/event-stream' in response.content_type:
        return response
    accept = request.headers.get('Accept-Encoding', '')
    if 'gzip' not in accept:
        return response
    ct = response.content_type or ''
    if not any(t in ct for t in ['text/', 'json', 'javascript', 'css', 'xml']):
        return response
    try:
        data = response.get_data()
        if len(data) < 500:
            return response
        compressed = gzip.compress(data, compresslevel=6)
        response.set_data(compressed)
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Content-Length'] = len(compressed)
    except Exception:
        pass
    return response


def sanitize_input(text):
    """清理用户输入，防止XSS"""
    if not text:
        return text
    text = str(text)
    text = re.sub(r'<[^>]+>', '', text)
    text = text.strip()[:100]
    return text


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapper


# ======================
# 首页 + 排盘
# ======================
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # CSRF 验证
        validate_csrf_token()

        birth_country = request.form.get("birth_country", "").strip()
        birth_date = request.form.get("birth_date", "").strip()
        birth_time = request.form.get("birth_time", "").strip() or None
        birth_city = request.form.get("birth_city", "").strip() or None
        name = request.form.get("name", "").strip()
        gender = request.form.get("gender", "").strip()
        unknown_time = request.form.get("unknown_time")

        # 统一处理出生时间不详
        if unknown_time:
            birth_time = None

        # 输入验证
        if birth_country not in VALID_COUNTRIES:
            return render_template("index.html", error="err_invalid_country")
        if not validate_birth_date(birth_date):
            return render_template("index.html", error="err_invalid_date")
        if birth_time and not validate_birth_time(birth_time):
            return render_template("index.html", error="err_invalid_time")
        if gender not in VALID_GENDERS:
            return render_template("index.html", error="err_invalid_gender")
        if name and not validate_name(name):
            return render_template("index.html", error="err_invalid_name")
        if birth_city and not validate_city(birth_city):
            return render_template("index.html", error="err_invalid_city")

        # 核心分析（带缓存）
        cache_params = dict(birth_country=birth_country, birth_date=birth_date,
                           birth_time=birth_time, gender=gender, city=birth_city)
        result = bazi_cache.get(**cache_params)
        if result is None:
            try:
                result = run_full_analysis_from_birth(**cache_params)
                bazi_cache.set(result, **cache_params)
            except Exception as e:
                logger.error(f"Bazi analysis error: {e}", exc_info=True)
                return render_template("index.html", error="err_bazi_calc")

        # 添加综合分析
        try:
            birth_year = int(birth_date[:4])
            day_master_gan = result.get("bazi_detail", {}).get("day", {}).get("gan", "甲")
            dm_elem = STEM_ELEMENT.get(day_master_gan, "木")
            dayun_data = result.get("dayun", [])
            result["dayun_comprehensive"] = analyze_dayun_comprehensive(dayun_data, birth_year, dm_elem)
            all_liunian = []
            for d in dayun_data:
                all_liunian.extend(d.get("liunian_list", []))
            result["liunian_comprehensive"] = analyze_liunian_comprehensive(all_liunian, birth_year, dm_elem)
        except Exception as e:
            logger.error(f"Comprehensive analysis error: {e}", exc_info=True)
            result["dayun_comprehensive"] = []
            result["liunian_comprehensive"] = []

        # 保存历史
        if "user_id" in session:
            try:
                chart = Chart(
                    user_id=session["user_id"],
                    name=sanitize_input(name),
                    birth_country=birth_country,
                    birth_date=birth_date,
                    birth_time=birth_time or "",
                    gender=gender,
                )
                chart.set_result(result)
                db.session.add(chart)
                db.session.commit()
            except Exception as e:
                logger.error(f"Save chart error: {e}", exc_info=True)
                db.session.rollback()

        return render_template("result.html", result=result, result_json=json.dumps(result, ensure_ascii=False))

    # GET
    # Handle ?load=ID — load a saved chart from history
    load_id = request.args.get("load")
    if load_id and "user_id" in session:
        try:
            chart = Chart.query.filter_by(id=int(load_id), user_id=session["user_id"]).first()
            if chart:
                result = chart.get_result()
                # Rebuild interpretation for fresh analysis
                try:
                    from core.interpretation_engine import build_comprehensive_interpretation
                    result["interpretation"] = build_comprehensive_interpretation(result)
                except Exception as e:
                    logger.error(f"Rebuild interpretation error: {e}", exc_info=True)
                result.setdefault("dayun_comprehensive", [])
                result.setdefault("liunian_comprehensive", [])
                # Rebuild comprehensive analysis
                try:
                    birth_date = None
                    for d in result.get("dayun", []):
                        if d.get("start_year"):
                            birth_date = str(d["start_year"])
                            break
                    day_master_gan = result.get("bazi_detail", {}).get("day", {}).get("gan", "甲")
                    dm_elem = STEM_ELEMENT.get(day_master_gan, "木")
                    if not result["dayun_comprehensive"]:
                        birth_year = int(birth_date) if birth_date else 1990
                        result["dayun_comprehensive"] = analyze_dayun_comprehensive(result.get("dayun", []), birth_year, dm_elem)
                except Exception as e:
                    logger.error(f"Rebuild comprehensive error: {e}", exc_info=True)
                for d in result.get("dayun", []):
                    d.setdefault("liunian_list", [])
                return render_template("result.html", result=result, result_json=json.dumps(result, ensure_ascii=False))
        except Exception as e:
            logger.error(f"Load chart error: {e}", exc_info=True)

    user_chart = None
    own_chart = None
    daily_fortune = None
    if "user_id" in session:
        try:
            charts = Chart.query.filter_by(
                user_id=session["user_id"]
            ).order_by(Chart.created_at.desc()).limit(3).all()
            user_chart = charts
            # 单独查询 is_own 的八字，确保一定存在
            own_chart = Chart.query.filter_by(
                user_id=session["user_id"], is_own=True
            ).first()
            if charts:
                latest_result = charts[0].get_result()
                daily_fortune = calc_daily_fortune(latest_result)
        except Exception as e:
            logger.error(f"Load history error: {e}", exc_info=True)

    return render_template("index.html", user_chart=user_chart, own_chart=own_chart, daily_fortune=daily_fortune)


# ======================
# 注册
# ======================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        validate_csrf_token()

        username = sanitize_input(request.form.get("username"))
        password = request.form.get("password", "")

        if not username or not password:
            return render_template("register.html", error="err_register_empty")

        if len(username) < 2 or len(username) > 20:
            return render_template("register.html", error="err_register_name_length")

        if len(password) < 8:
            return render_template("register.html", error="err_register_password_length")

        # 密码强度检查
        if not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password):
            return render_template("register.html", error="err_register_password_strength")

        if User.query.filter_by(username=username).first():
            return render_template("register.html", error="err_register_name_exists")

        try:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return redirect("/login")
        except Exception as e:
            logger.error(f"Register error: {e}", exc_info=True)
            db.session.rollback()
            return render_template("register.html", error="err_register_fail")

    return render_template("register.html")


# ======================
# 登录（含暴力破解保护）
# ======================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        validate_csrf_token()

        # 检查登录限流
        allowed, remaining = check_login_rate_limit()
        if not allowed:
            session['rate_limit_remaining'] = remaining
            return render_template("login.html", error="err_login_rate_limit")

        username = sanitize_input(request.form.get("username"))
        password = request.form.get("password", "")

        if not username or not password:
            return render_template("login.html", error="err_login_empty")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            reset_login_attempts()
            session.clear()
            session.permanent = True
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect("/")

        record_login_attempt()
        return render_template("login.html", error="err_login_wrong")

    return render_template("login.html")


# ======================
# 登出
# ======================
@app.route("/logout", methods=["POST"])
def logout():
    validate_csrf_token()
    session.clear()
    return redirect("/")


# ======================
# 历史记录
# ======================
@app.route("/history")
@login_required
def history():
    try:
        page = request.args.get("page", 1, type=int)
        per_page = 10
        pagination = Chart.query.filter_by(
            user_id=session["user_id"]
        ).order_by(Chart.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        return render_template("history.html", history=pagination.items, pagination=pagination)
    except Exception as e:
        logger.error(f"History query error: {e}", exc_info=True)
        return render_template("history.html", history=[], pagination=None)


# ======================
# 设置/取消我的八字
# ======================
@app.route("/api/set-own/<int:chart_id>", methods=["POST"])
@login_required
def set_own_chart(chart_id):
    try:
        chart = Chart.query.filter_by(id=chart_id, user_id=session["user_id"]).first()
        if not chart:
            return jsonify({"error": "not found"}), 404
        # 取消其他所有 is_own
        Chart.query.filter_by(user_id=session["user_id"], is_own=True).update({"is_own": False})
        # 设置当前为 is_own
        chart.is_own = True
        db.session.commit()
        return jsonify({"ok": True})
    except Exception as e:
        logger.error(f"Set own chart error: {e}", exc_info=True)
        db.session.rollback()
        return jsonify({"error": "failed"}), 500


@app.route("/api/unset-own/<int:chart_id>", methods=["POST"])
@login_required
def unset_own_chart(chart_id):
    try:
        chart = Chart.query.filter_by(id=chart_id, user_id=session["user_id"]).first()
        if not chart:
            return jsonify({"error": "not found"}), 404
        chart.is_own = False
        db.session.commit()
        return jsonify({"ok": True})
    except Exception as e:
        logger.error(f"Unset own chart error: {e}", exc_info=True)
        db.session.rollback()
        return jsonify({"error": "failed"}), 500


# ======================
# AI 分析接口
# ======================
@app.route("/api/ai-analysis", methods=["POST"])
@login_required
def ai_analysis():
    data = request.get_json(silent=True)
    if not data:
        return safe_error_response("error_invalid_request", 400)

    result = data.get("result")
    lang = data.get("lang", "zh")
    stream = data.get("stream", False)

    # 验证 lang 参数
    if lang not in ("zh", "en", "ja", "ko", "vi"):
        lang = "zh"

    if not result or not isinstance(result, dict):
        return safe_error_response("error_missing_bazi_data", 400)

    if not validate_result_dict(result):
        return safe_error_response("error_invalid_result", 400)

    # 用户级限流（防止滥用 AI API）
    user_id = session.get("user_id")
    if user_id and not check_user_api_rate_limit(user_id):
        return safe_error_response("error_rate_limit", 429)

    if stream:
        def generate():
            for chunk in generate_ai_analysis_stream(result, lang):
                yield chunk
        return Response(generate(), mimetype="text/event-stream")
    else:
        response = generate_ai_analysis(result, lang)
        return jsonify(response)


# ======================
# 分享卡片生成
# ======================
@app.route("/api/share-card", methods=["POST"])
def share_card():
    if not HAS_PILLOW:
        return safe_error_response("error_sharecard_disabled", 501)

    data = request.get_json(silent=True)
    if not data:
        return safe_error_response("error_invalid_request", 400)

    result = data.get("result")
    if not result or not isinstance(result, dict):
        return safe_error_response("error_missing_bazi_data", 400)

    if not validate_result_dict(result):
        return safe_error_response("error_invalid_result", 400)

    tmp_path = None
    try:
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = tmp.name
        generate_share_card(result, tmp_path)
        with open(tmp_path, 'rb') as f:
            img_data = f.read()
        return Response(img_data, mimetype="image/png", headers={
            "Content-Disposition": "attachment; filename=bazi_card.png"
        })
    except Exception as e:
        logger.error(f"Share card error: {e}", exc_info=True)
        return safe_error_response("error_sharecard_failed", 500)
    finally:
        # 清理临时文件
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except OSError:
                pass


# ======================
# 每日运势
# ======================
@app.route("/api/daily-fortune", methods=["POST"])
def daily_fortune():
    data = request.get_json(silent=True)
    if not data:
        return safe_error_response("error_invalid_request", 400)

    result = data.get("result")
    if not result or not isinstance(result, dict):
        return safe_error_response("error_missing_bazi_data", 400)

    if not validate_result_dict(result):
        return safe_error_response("error_invalid_result", 400)

    date_str = data.get("date")

    try:
        from datetime import date as date_cls
        target_date = None
        if date_str:
            # 验证日期格式
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', str(date_str)):
                return safe_error_response("error_invalid_date_format", 400)
            target_date = date_cls.fromisoformat(str(date_str))
        fortune = calc_daily_fortune(result, target_date)
        return jsonify(fortune)
    except ValueError:
        return safe_error_response("error_invalid_date_format", 400)
    except Exception as e:
        logger.error(f"Daily fortune error: {e}", exc_info=True)
        return safe_error_response("error_fortune_calc_failed", 500)


@app.route("/api/weekly-fortune", methods=["POST"])
def weekly_fortune():
    data = request.get_json(silent=True)
    if not data:
        return safe_error_response("error_invalid_request", 400)

    result = data.get("result")
    if not result or not isinstance(result, dict):
        return safe_error_response("error_missing_bazi_data", 400)

    if not validate_result_dict(result):
        return safe_error_response("error_invalid_result", 400)

    try:
        fortune = calc_weekly_fortune(result)
        return jsonify({"days": fortune})
    except Exception as e:
        logger.error(f"Weekly fortune error: {e}", exc_info=True)
        return safe_error_response("error_fortune_calc_failed", 500)


@app.route("/api/monthly-fortune", methods=["POST"])
def monthly_fortune():
    data = request.get_json(silent=True)
    if not data:
        return safe_error_response("error_invalid_request", 400)

    result = data.get("result")
    if not result or not isinstance(result, dict):
        return safe_error_response("error_missing_bazi_data", 400)

    if not validate_result_dict(result):
        return safe_error_response("error_invalid_result", 400)

    year = data.get("year")
    month = data.get("month")

    try:
        fortune = calc_monthly_fortune(result, year, month)
        return jsonify(fortune)
    except Exception as e:
        logger.error(f"Monthly fortune error: {e}", exc_info=True)
        return safe_error_response("error_fortune_calc_failed", 500)


# ======================
# 双人合盘
# ======================
@app.route("/api/compatibility", methods=["POST"])
def compatibility():
    data = request.get_json(silent=True)
    if not data:
        return safe_error_response("error_invalid_request", 400)

    result1 = data.get("result1")
    result2 = data.get("result2")

    if not result1 or not result2 or not isinstance(result1, dict) or not isinstance(result2, dict):
        return safe_error_response("error_missing_two_results", 400)

    try:
        lang = data.get("lang", session.get("lang", "zh"))
        analysis = analyze_compatibility(result1, result2, lang=lang)
        return jsonify(analysis)
    except Exception as e:
        logger.error(f"Compatibility error: {e}", exc_info=True)
        return safe_error_response("error_compat_failed", 500)


# ======================
# PDF 导出
# ======================
@app.route("/api/export-pdf", methods=["POST"])
def export_pdf():
    if not HAS_REPORTLAB:
        return safe_error_response("error_pdf_disabled", 501)

    data = request.get_json(silent=True)
    if not data:
        return safe_error_response("error_invalid_request", 400)

    result = data.get("result")
    if not result or not isinstance(result, dict):
        return safe_error_response("error_missing_bazi_data", 400)

    if not validate_result_dict(result):
        return safe_error_response("error_invalid_result", 400)

    try:
        pdf_buffer = generate_pdf_report(result)
        return Response(
            pdf_buffer.getvalue(),
            mimetype="application/pdf",
            headers={"Content-Disposition": "attachment; filename=bazi_report.pdf"}
        )
    except Exception as e:
        logger.error(f"PDF export error: {e}", exc_info=True)
        return safe_error_response("error_pdf_failed", 500)


# ======================
# 系统说明
# ======================
@app.route("/explain")
def explain():
    return render_template("explain.html")


# ======================
# 付费咨询页
# ======================
@app.route("/consult")
def consult():
    return render_template("consult.html")


@app.route("/glossary")
def glossary():
    return render_template("glossary.html")


@app.route("/liunian")
def liunian():
    return render_template("liunian.html", overview=[])


@app.route("/dashboard")
def dashboard():
    user_id = session.get('user_id')
    charts = []
    if user_id:
        from models.chart import Chart
        charts = Chart.query.filter_by(user_id=user_id).order_by(Chart.created_at.desc()).all()
    return render_template("dashboard.html", charts=charts)


@app.route("/set_lang/<lang>")
def set_lang(lang):
    if lang in ('zh', 'ja', 'en', 'ko', 'vi', 'my'):
        session['lang'] = lang
    next_url = request.args.get('next', '/')
    # Prevent open redirect: only allow relative paths on the same host
    if not next_url.startswith('/') or next_url.startswith('//'):
        next_url = '/'
    return redirect(next_url)


# ======================
# Favicon（避免 404）
# ======================
@app.route("/favicon.ico")
def favicon():
    # 返回一个简单的太极图标 SVG
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
      <circle cx="50" cy="50" r="48" fill="#0c0a08" stroke="#c9a84c" stroke-width="2"/>
      <path d="M50 2 A48 48 0 0 1 50 98 A24 24 0 0 1 50 50 A24 24 0 0 0 50 2" fill="#e8dcc8"/>
      <circle cx="50" cy="26" r="6" fill="#0c0a08"/>
      <circle cx="50" cy="74" r="6" fill="#e8dcc8"/>
    </svg>'''
    return Response(svg, mimetype="image/svg+xml")


# ======================
# 缓存统计
# ======================
@app.route("/api/cache-stats")
def cache_stats():
    return jsonify(bazi_cache.stats())


# ======================
# 404 处理
# ======================
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return safe_error_response("error_method_not_allowed", 405)


@app.errorhandler(413)
def request_entity_too_large(e):
    return safe_error_response("error_payload_too_large", 413)


@app.errorhandler(429)
def too_many_requests(e):
    return safe_error_response("error_too_many_requests", 429)


@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Internal server error: {e}")
    db.session.rollback()
    return safe_error_response("error_internal_server", 500)


# ======================
# 数据库初始化
# ======================
@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("Database initialized.")


if os.environ.get('FLASK_ENV') == 'production' and os.environ.get('FLASK_DEBUG') == 'true':
    logger.warning('FLASK_DEBUG=true in production is a security risk. Forcing debug off.')
    app.debug = False
    os.environ['FLASK_DEBUG'] = 'false'

if __name__ == "__main__":
    # 绝对不要在生产环境使用 debug=True
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(debug=debug_mode)
