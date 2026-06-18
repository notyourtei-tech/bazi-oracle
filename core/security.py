
# core/security.py
# 安全模块：CSRF保护、输入验证、安全加固

import os
import secrets
import time
import re
from functools import wraps
from flask import session, request, abort, jsonify

# ========================
# CSRF 保护
# ========================

def generate_csrf_token():
    """生成CSRF token并存入session"""
    if '_csrf_token' not in session:
        session['_csrf_token'] = secrets.token_hex(32)
    return session['_csrf_token']

def validate_csrf_token():
    """验证CSRF token"""
    token = session.get('_csrf_token')
    form_token = request.form.get('_csrf_token') or request.headers.get('X-CSRF-Token')
    if not token or not form_token or token != form_token:
        abort(403)

def csrf_protect(f):
    """CSRF保护装饰器"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.method in ('POST', 'PUT', 'DELETE', 'PATCH'):
            validate_csrf_token()
        return f(*args, **kwargs)
    return wrapper


# ========================
# 登录暴力破解保护
# ========================

_login_attempts = {}  # {ip: [timestamp, ...]}
LOGIN_RATE_LIMIT = 5  # 每分钟最多5次登录尝试
LOGIN_LOCKOUT_SECONDS = 300  # 锁定5分钟

def check_login_rate_limit():
    """检查登录限流"""
    ip = request.remote_addr
    now = time.time()
    if ip not in _login_attempts:
        _login_attempts[ip] = []
    # 清理过期记录
    _login_attempts[ip] = [t for t in _login_attempts[ip] if now - t < 60]
    # 检查是否被锁定
    if len(_login_attempts[ip]) >= LOGIN_RATE_LIMIT:
        # 检查最近一次尝试是否在锁定期内
        if now - _login_attempts[ip][-1] < LOGIN_LOCKOUT_SECONDS:
            remaining = int(LOGIN_LOCKOUT_SECONDS - (now - _login_attempts[ip][-1]))
            return False, remaining
    return True, 0

def record_login_attempt():
    """记录登录尝试"""
    ip = request.remote_addr
    now = time.time()
    if ip not in _login_attempts:
        _login_attempts[ip] = []
    _login_attempts[ip].append(now)

def reset_login_attempts():
    """登录成功后重置尝试次数"""
    ip = request.remote_addr
    _login_attempts.pop(ip, None)


# ========================
# 请求限流器（修复内存泄漏）
# ========================

_request_counts = {}
RATE_LIMIT = 30
RATE_WINDOW = 60
_last_cleanup = time.time()
CLEANUP_INTERVAL = 300  # 每5分钟清理一次

def check_rate_limit():
    """请求限流，带自动清理"""
    global _last_cleanup
    ip = request.remote_addr
    now = time.time()
    
    # 定期清理过期IP记录，防止内存泄漏
    if now - _last_cleanup > CLEANUP_INTERVAL:
        expired_ips = [k for k, v in _request_counts.items() if not v or now - v[-1] > RATE_WINDOW]
        for ip_key in expired_ips:
            del _request_counts[ip_key]
        _last_cleanup = now
    
    if ip not in _request_counts:
        _request_counts[ip] = []
    _request_counts[ip] = [t for t in _request_counts[ip] if now - t < RATE_WINDOW]
    if len(_request_counts[ip]) >= RATE_LIMIT:
        return False
    _request_counts[ip].append(now)
    return True


# ========================
# 输入验证
# ========================

VALID_COUNTRIES = {
    "CN", "JP", "KR", "TW", "HK", "MO", "MN",
    "VN", "TH", "PH", "MY", "SG", "ID", "MM", "KH", "LA", "BN",
    "IN", "PK", "BD", "LK", "NP", "MV",
    "TR", "SA", "AE", "QA", "KW", "BH", "OM", "IL", "JO", "LB", "IQ", "IR", "KZ", "UZ",
    "GB", "DE", "FR", "IT", "ES", "PT", "NL", "BE", "CH", "AT", "SE", "NO", "DK", "FI",
    "PL", "CZ", "GR", "IE", "RO", "UA", "HU", "RU",
    "US", "CA", "MX", "GT", "CU", "JM", "PA",
    "BR", "AR", "CL", "CO", "PE", "VE", "EC",
    "EG", "ZA", "NG", "KE", "GH", "MA", "ET", "TZ", "DZ",
    "AU", "NZ", "FJ",
}

VALID_GENDERS = {"male", "female"}

def validate_birth_date(date_str):
    """验证出生日期格式 YYYY-MM-DD"""
    if not date_str:
        return False
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, date_str):
        return False
    try:
        y, m, d = map(int, date_str.split('-'))
        if y < 1 or y > 2200:
            return False
        if m < 1 or m > 12:
            return False
        if d < 1 or d > 31:
            return False
        return True
    except (ValueError, TypeError):
        return False

def validate_birth_time(time_str):
    """验证出生时间格式 HH:MM"""
    if not time_str:
        return True  # 可选字段
    pattern = r'^\d{2}:\d{2}$'
    if not re.match(pattern, time_str):
        return False
    try:
        h, m = map(int, time_str.split(':'))
        return 0 <= h <= 23 and 0 <= m <= 59
    except (ValueError, TypeError):
        return False

def validate_name(name):
    """验证姓名"""
    if not name:
        return True  # 可选
    if len(name) > 50:
        return False
    # 只允许中文、字母、数字、空格
    return bool(re.match(r'^[\u4e00-\u9fa5a-zA-Z0-9\s]+$', name))


# ========================
# 安全的错误响应
# ========================

def safe_error_response(message, status_code=400):
    """返回安全的错误响应，不泄露内部信息"""
    return jsonify({"error": message}), status_code


# ========================
# 临时文件清理
# ========================

import tempfile
import atexit
import os

_cleanup_files = []

def register_temp_file(filepath):
    """注册临时文件，程序退出时自动清理"""
    _cleanup_files.append(filepath)

def _cleanup_temp_files():
    """清理所有注册的临时文件"""
    for f in _cleanup_files:
        try:
            if os.path.exists(f):
                os.unlink(f)
        except OSError:
            pass

atexit.register(_cleanup_temp_files)
