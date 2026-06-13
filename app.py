from flask import Flask, render_template, request, redirect, session, Response, jsonify, send_file, abort
from functools import wraps
import json
import io
import re
import secrets
from datetime import timedelta

from models.user import db, User
from models.chart import Chart

# 你已有的分析入口
from core.pipeline import run_full_analysis_from_birth
from core.ai_engine import generate_ai_analysis, generate_ai_analysis_stream
from core.share_card import generate_share_card, HAS_PILLOW
from core.daily_fortune_engine import calc_daily_fortune, calc_weekly_fortune, calc_monthly_fortune
from core.compatibility_engine import analyze_compatibility
from core.pdf_engine import generate_pdf_report, HAS_REPORTLAB
from core.comprehensive_analysis import analyze_dayun_comprehensive, analyze_liunian_comprehensive, STEM_ELEMENT

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# 安全配置
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=30)
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024  # 1MB 上传限制

db.init_app(app)

# 请求限流器（简单的内存限流）
request_counts = {}
RATE_LIMIT = 30  # 每分钟最多30次请求
RATE_WINDOW = 60  # 60秒窗口

def check_rate_limit():
    """简单的请求限流"""
    import time
    ip = request.remote_addr
    now = time.time()
    if ip not in request_counts:
        request_counts[ip] = []
    # 清理过期记录
    request_counts[ip] = [t for t in request_counts[ip] if now - t < RATE_WINDOW]
    if len(request_counts[ip]) >= RATE_LIMIT:
        return False
    request_counts[ip].append(now)
    return True

@app.before_request
def before_request():
    """请求前安全检查"""
    if not check_rate_limit():
        return jsonify({"error": "Too many requests"}), 429
    
    # 阻止常见攻击路径
    blocked_paths = ['/wp-admin', '/phpmyadmin', '/.env', '/config', '/backup']
    for path in blocked_paths:
        if request.path.lower().startswith(path):
            abort(404)

@app.after_request
def after_request(response):
    """添加安全响应头"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self' 'unsafe-inline' 'unsafe-eval'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'"
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), camera=(), microphone=()'
    return response

def sanitize_input(text):
    """清理用户输入，防止XSS"""
    if not text:
        return text
    text = str(text)
    text = re.sub(r'<[^>]+>', '', text)  # 移除HTML标签
    text = text.strip()[:100]  # 限制长度
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
        birth_country = request.form.get("birth_country")
        birth_date = request.form.get("birth_date")
        birth_time = request.form.get("birth_time")
        birth_city = request.form.get("birth_city") or None
        name = request.form.get("name")
        gender = request.form.get("gender")
        unknown_time = request.form.get("unknown_time")

        # 统一处理出生时间不详
        if unknown_time:
            birth_time = None

        # 核心分析（按出生地真太阳时计算）
        result = run_full_analysis_from_birth(
            birth_country=birth_country,
            birth_date=birth_date,
            birth_time=birth_time,
            gender=gender,
            city=birth_city
        )
        
        # 添加综合分析
        try:
            birth_year = int(birth_date[:4])
            day_master_gan = result.get("bazi_detail", {}).get("day", {}).get("gan", "甲")
            dm_elem = STEM_ELEMENT.get(day_master_gan, "木")
            
            # 综合大运分析
            dayun_data = result.get("dayun", [])
            result["dayun_comprehensive"] = analyze_dayun_comprehensive(dayun_data, birth_year, dm_elem)
            
            # 综合流年分析（取每个大运的流年）
            all_liunian = []
            for d in dayun_data:
                all_liunian.extend(d.get("liunian_list", []))
            result["liunian_comprehensive"] = analyze_liunian_comprehensive(all_liunian, birth_year, dm_elem)
        except Exception as e:
            result["dayun_comprehensive"] = []
            result["liunian_comprehensive"] = []

        # 如果已登录 → 保存历史
        if "user_id" in session:
            chart = Chart(
                user_id=session["user_id"],
                name=name,
                birth_country=birth_country,
                birth_date=birth_date,
                birth_time=birth_time or "",
                gender=gender,
                result_json=json.dumps(result, ensure_ascii=False)
            )
            db.session.add(chart)
            db.session.commit()

        return render_template("result.html", result=result, result_json=json.dumps(result, ensure_ascii=False))

    # GET: 首页 - 获取用户数据
    user_chart = None
    daily_fortune = None
    if "user_id" in session:
        charts = Chart.query.filter_by(user_id=session["user_id"]).order_by(Chart.created_at.desc()).limit(3).all()
        user_chart = charts
        
        # 获取最新命盘的运势
        if charts:
            try:
                latest_result = json.loads(charts[0].result_json)
                daily_fortune = calc_daily_fortune(latest_result)
            except:
                pass

    return render_template("index.html", user_chart=user_chart, daily_fortune=daily_fortune)


# ======================
# 注册
# ======================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = sanitize_input(request.form.get("username"))
        password = request.form.get("password")

        if not username or not password:
            return render_template("register.html", error="请填写完整信息")
        
        if len(username) < 1 or len(username) > 20:
            return render_template("register.html", error="姓名长度为1-20个字符")
        
        if len(password) < 6:
            return render_template("register.html", error="密码至少6位")

        if User.query.filter_by(username=username).first():
            return render_template("register.html", error="该姓名已被注册")

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")


# ======================
# 登录
# ======================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = sanitize_input(request.form.get("username"))
        password = request.form.get("password")

        if not username or not password:
            return render_template("login.html", error="请填写完整信息")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session.permanent = True
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect("/")

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
# 历史记录（登录后）
# ======================
@app.route("/history")
@login_required
def history():
    records = Chart.query.filter_by(
        user_id=session["user_id"]
    ).order_by(Chart.created_at.desc()).all()

    return render_template("history.html", history=records)


# ======================
# AI 分析接口
# ======================
@app.route("/api/ai-analysis", methods=["POST"])
def ai_analysis():
    """Generate personalized AI analysis for bazi result."""
    data = request.get_json()
    result = data.get("result")
    lang = data.get("lang", "zh")
    stream = data.get("stream", False)

    if not result:
        return jsonify({"error": "No bazi result provided"}), 400

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
    """Generate shareable bazi analysis card image."""
    if not HAS_PILLOW:
        return jsonify({"error": "Share card requires Pillow library"}), 501
    
    data = request.get_json()
    result = data.get("result")
    
    if not result:
        return jsonify({"error": "No bazi result provided"}), 400
    
    try:
        img_buffer = io.BytesIO()
        from PIL import Image
        import base64
        
        # Generate card to temp file, then return as response
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            generate_share_card(result, tmp.name)
            tmp.seek(0)
            img_data = tmp.read()
        
        return Response(img_data, mimetype="image/png", headers={
            "Content-Disposition": "attachment; filename=bazi_card.png"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ======================
# 每日运势
# ======================
@app.route("/api/daily-fortune", methods=["POST"])
def daily_fortune():
    """Calculate daily fortune for a bazi chart."""
    data = request.get_json()
    result = data.get("result")
    date_str = data.get("date")  # Optional: YYYY-MM-DD
    
    if not result:
        return jsonify({"error": "No bazi result provided"}), 400
    
    try:
        from datetime import date as date_cls
        target_date = date_cls.fromisoformat(date_str) if date_str else None
        fortune = calc_daily_fortune(result, target_date)
        return jsonify(fortune)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/weekly-fortune", methods=["POST"])
def weekly_fortune():
    """Calculate weekly fortune for a bazi chart."""
    data = request.get_json()
    result = data.get("result")
    
    if not result:
        return jsonify({"error": "No bazi result provided"}), 400
    
    try:
        fortune = calc_weekly_fortune(result)
        return jsonify({"days": fortune})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ======================
# 双人合盘
# ======================
@app.route("/api/compatibility", methods=["POST"])
def compatibility():
    """Analyze compatibility between two bazi charts."""
    data = request.get_json()
    result1 = data.get("result1")
    result2 = data.get("result2")
    
    if not result1 or not result2:
        return jsonify({"error": "Both bazi results are required"}), 400
    
    try:
        analysis = analyze_compatibility(result1, result2)
        return jsonify(analysis)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ======================
# PDF 导出
# ======================
@app.route("/api/export-pdf", methods=["POST"])
def export_pdf():
    """Generate PDF report for bazi analysis."""
    if not HAS_REPORTLAB:
        return jsonify({"error": "PDF generation requires reportlab library"}), 501
    
    data = request.get_json()
    result = data.get("result")
    
    if not result:
        return jsonify({"error": "No bazi result provided"}), 400
    
    try:
        pdf_buffer = generate_pdf_report(result)
        return Response(
            pdf_buffer.getvalue(),
            mimetype="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=bazi_report.pdf"
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ======================
# 系统说明
# ======================
@app.route("/explain")
def explain():
    return render_template("explain.html")


# ======================
# 初始化数据库（第一次用）
# ======================
@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("Database initialized.")


if __name__ == "__main__":
    app.run(debug=True)
