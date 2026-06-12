from flask import Flask, render_template, request, redirect, session
from functools import wraps
import json

from models.user import db, User
from models.chart import Chart

# 你已有的分析入口
from core.pipeline import run_full_analysis_from_birth

app = Flask(__name__)
app.secret_key = "replace_this_with_random_secret"

# 数据库配置
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


# ======================
# 工具：登录保护
# ======================
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

        return render_template("result.html", result=result)

    return render_template("index.html")


# ======================
# 注册
# ======================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("email") or request.form.get("username")
        password = request.form.get("password")

        if User.query.filter_by(username=username).first():
            return "User already exists"

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
        username = request.form.get("email") or request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            return redirect("/")

        return "Login failed"

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
