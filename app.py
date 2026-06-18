from flask import Flask, render_template, request, redirect, session, Response, jsonify, send_file, abort
from functools import wraps
from dotenv import load_dotenv
import json
import io
import os
import re
import secrets
import logging
from datetime import timedelta

from models.user import db, User
from models.chart import Chart

from core.pipeline import run_full_analysis_from_birth
from core.ai_engine import generate_ai_analysis, generate_ai_analysis_stream
from core.share_card import generate_share_card, HAS_PILLOW
from core.daily_fortune_engine import calc_daily_fortune, calc_weekly_fortune, calc_monthly_fortune
from core.compatibility_engine import analyze_compatibility
from core.pdf_engine import generate_pdf_report, HAS_REPORTLAB
from core.comprehensive_analysis import analyze_dayun_comprehensive, analyze_liunian_comprehensive, STEM_ELEMENT
from core.security import (
    generate_csrf_token, csrf_protect, check_rate_limit,
    check_login_rate_limit, record_login_attempt, reset_login_attempts,
    validate_birth_date, validate_birth_time, validate_name,
    validate_csrf_token, safe_error_response, VALID_COUNTRIES, VALID_GENDERS,
    register_temp_file
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

# 密钥：优先从环境变量读取，否则每次启动随机生成（开发环境）
app.secret_key = os.environ.get('SECRET_KEY') or secrets.token_hex(32)

# 数据库
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Session 安全
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=30)

# 仅在生产环境启用 Secure flag（需要 HTTPS）
if os.environ.get('FLASK_ENV') == 'production' or os.environ.get('FORCE_HTTPS'):
    app.config["SESSION_COOKIE_SECURE"] = True

# 上传限制
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024  # 1MB

db.init_app(app)

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
        return safe_error_response("请求过于频繁，请稍后再试", 429)

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

    # 开发环境：禁止浏览器缓存HTML，确保始终获取最新内容
    if request.path.endswith('.html') or request.path == '/' or request.path == '':
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

        # 核心分析
        try:
            result = run_full_analysis_from_birth(
                birth_country=birth_country,
                birth_date=birth_date,
                birth_time=birth_time,
                gender=gender,
                city=birth_city
            )
        except Exception as e:
            logger.error(f"Bazi analysis error: {type(e).__name__}")
            return render_template("index.html", error="排盘计算出错，请检查输入信息后重试")

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
            logger.error(f"Comprehensive analysis error: {type(e).__name__}")
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
                    result_json=json.dumps(result, ensure_ascii=False)
                )
                db.session.add(chart)
                db.session.commit()
            except Exception as e:
                logger.error(f"Save chart error: {type(e).__name__}")
                db.session.rollback()

        return render_template("result.html", result=result, result_json=json.dumps(result, ensure_ascii=False))

    # GET
    # Handle ?load=ID — load a saved chart from history
    load_id = request.args.get("load")
    if load_id and "user_id" in session:
        try:
            chart = Chart.query.filter_by(id=int(load_id), user_id=session["user_id"]).first()
            if chart:
                result = json.loads(chart.result_json)
                # Rebuild interpretation for fresh analysis
                try:
                    from core.interpretation_engine import build_comprehensive_interpretation
                    result["interpretation"] = build_comprehensive_interpretation(result)
                except Exception as e:
                    logger.error(f"Rebuild interpretation error: {e}")
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
                    from core.comprehensive_analysis import STEM_ELEMENT
                    dm_elem = STEM_ELEMENT.get(day_master_gan, "木")
                    if not result["dayun_comprehensive"]:
                        birth_year = int(birth_date) if birth_date else 1990
                        result["dayun_comprehensive"] = analyze_dayun_comprehensive(result.get("dayun", []), birth_year, dm_elem)
                except Exception as e:
                    logger.error(f"Rebuild comprehensive error: {e}")
                for d in result.get("dayun", []):
                    d.setdefault("liunian_list", [])
                return render_template("result.html", result=result, result_json=json.dumps(result, ensure_ascii=False))
        except Exception as e:
            logger.error(f"Load chart error: {type(e).__name__}: {e}")

    user_chart = None
    daily_fortune = None
    if "user_id" in session:
        try:
            charts = Chart.query.filter_by(
                user_id=session["user_id"]
            ).order_by(Chart.created_at.desc()).limit(3).all()
            user_chart = charts
            if charts:
                latest_result = json.loads(charts[0].result_json)
                daily_fortune = calc_daily_fortune(latest_result)
        except Exception as e:
            logger.error(f"Load history error: {type(e).__name__}")

    return render_template("index.html", user_chart=user_chart, daily_fortune=daily_fortune)


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
            return render_template("register.html", error="请填写完整信息")

        if len(username) < 2 or len(username) > 20:
            return render_template("register.html", error="姓名长度为2-20个字符")

        if len(password) < 8:
            return render_template("register.html", error="密码至少8位")

        # 密码强度检查
        if not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password):
            return render_template("register.html", error="密码必须包含字母和数字")

        if User.query.filter_by(username=username).first():
            return render_template("register.html", error="该姓名已被注册")

        try:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return redirect("/login")
        except Exception as e:
            logger.error(f"Register error: {type(e).__name__}")
            db.session.rollback()
            return render_template("register.html", error="注册失败，请重试")

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
            return render_template("login.html", error=f"登录尝试过多，请{remaining}秒后重试")

        username = sanitize_input(request.form.get("username"))
        password = request.form.get("password", "")

        if not username or not password:
            return render_template("login.html", error="请填写完整信息")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            reset_login_attempts()
            session.permanent = True
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect("/")

        record_login_attempt()
        return render_template("login.html", error="姓名或密码错误")

    return render_template("login.html")


# ======================
# 登出
# ======================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ======================
# 历史记录
# ======================
@app.route("/history")
@login_required
def history():
    try:
        records = Chart.query.filter_by(
            user_id=session["user_id"]
        ).order_by(Chart.created_at.desc()).all()
        return render_template("history.html", history=records)
    except Exception as e:
        logger.error(f"History query error: {type(e).__name__}")
        return render_template("history.html", history=[])


# ======================
# AI 分析接口
# ======================
@app.route("/api/ai-analysis", methods=["POST"])
def ai_analysis():
    data = request.get_json(silent=True)
    if not data:
        return safe_error_response("无效的请求", 400)

    result = data.get("result")
    lang = data.get("lang", "zh")
    stream = data.get("stream", False)

    # 验证 lang 参数
    if lang not in ("zh", "en", "ja", "ko", "vi"):
        lang = "zh"

    if not result or not isinstance(result, dict):
        return safe_error_response("缺少八字数据", 400)

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
        return safe_error_response("分享卡功能未启用", 501)

    data = request.get_json(silent=True)
    if not data:
        return safe_error_response("无效的请求", 400)

    result = data.get("result")
    if not result or not isinstance(result, dict):
        return safe_error_response("缺少八字数据", 400)

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
        logger.error(f"Share card error: {type(e).__name__}")
        return safe_error_response("分享卡生成失败", 500)
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
        return safe_error_response("无效的请求", 400)

    result = data.get("result")
    if not result or not isinstance(result, dict):
        return safe_error_response("缺少八字数据", 400)

    date_str = data.get("date")

    try:
        from datetime import date as date_cls
        target_date = None
        if date_str:
            # 验证日期格式
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', str(date_str)):
                return safe_error_response("日期格式无效", 400)
            target_date = date_cls.fromisoformat(str(date_str))
        fortune = calc_daily_fortune(result, target_date)
        return jsonify(fortune)
    except ValueError:
        return safe_error_response("日期格式无效", 400)
    except Exception as e:
        logger.error(f"Daily fortune error: {type(e).__name__}")
        return safe_error_response("运势计算失败", 500)


@app.route("/api/weekly-fortune", methods=["POST"])
def weekly_fortune():
    data = request.get_json(silent=True)
    if not data:
        return safe_error_response("无效的请求", 400)

    result = data.get("result")
    if not result or not isinstance(result, dict):
        return safe_error_response("缺少八字数据", 400)

    try:
        fortune = calc_weekly_fortune(result)
        return jsonify({"days": fortune})
    except Exception as e:
        logger.error(f"Weekly fortune error: {type(e).__name__}")
        return safe_error_response("运势计算失败", 500)


# ======================
# 双人合盘
# ======================
@app.route("/api/compatibility", methods=["POST"])
def compatibility():
    data = request.get_json(silent=True)
    if not data:
        return safe_error_response("无效的请求", 400)

    result1 = data.get("result1")
    result2 = data.get("result2")

    if not result1 or not result2 or not isinstance(result1, dict) or not isinstance(result2, dict):
        return safe_error_response("需要提供两个人的八字数据", 400)

    try:
        analysis = analyze_compatibility(result1, result2)
        return jsonify(analysis)
    except Exception as e:
        logger.error(f"Compatibility error: {type(e).__name__}")
        return safe_error_response("合盘分析失败", 500)


# ======================
# PDF 导出
# ======================
@app.route("/api/export-pdf", methods=["POST"])
def export_pdf():
    if not HAS_REPORTLAB:
        return safe_error_response("PDF导出功能未启用", 501)

    data = request.get_json(silent=True)
    if not data:
        return safe_error_response("无效的请求", 400)

    result = data.get("result")
    if not result or not isinstance(result, dict):
        return safe_error_response("缺少八字数据", 400)

    try:
        pdf_buffer = generate_pdf_report(result)
        return Response(
            pdf_buffer.getvalue(),
            mimetype="application/pdf",
            headers={"Content-Disposition": "attachment; filename=bazi_report.pdf"}
        )
    except Exception as e:
        logger.error(f"PDF export error: {type(e).__name__}")
        return safe_error_response("PDF导出失败", 500)


# ======================
# 系统说明
# ======================
@app.route("/explain")
def explain():
    return render_template("explain.html")


# ======================
# 404 处理
# ======================
@app.errorhandler(404)
def not_found(e):
    return render_template("base.html"), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return safe_error_response("请求方法不允许", 405)


@app.errorhandler(413)
def request_entity_too_large(e):
    return safe_error_response("请求内容过大", 413)


@app.errorhandler(429)
def too_many_requests(e):
    return safe_error_response("请求过于频繁", 429)


@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Internal server error: {e}")
    db.session.rollback()
    return safe_error_response("服务器内部错误", 500)


# ======================
# 数据库初始化
# ======================
@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("Database initialized.")


if __name__ == "__main__":
    # 绝对不要在生产环境使用 debug=True
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(debug=debug_mode)
