import os
import secrets


def _get_secret_key():
    """获取密钥：优先环境变量，否则生成并持久化到 instance/.secret_key"""
    key = os.environ.get('SECRET_KEY')
    if key:
        return key
    # 尝试从 instance 目录读取已有密钥
    instance_dir = os.path.join(os.path.dirname(__file__), 'instance')
    os.makedirs(instance_dir, exist_ok=True)
    key_file = os.path.join(instance_dir, '.secret_key')
    if os.path.exists(key_file):
        with open(key_file, 'r') as f:
            return f.read().strip()
    # 首次生成，写入文件
    key = secrets.token_hex(32)
    with open(key_file, 'w') as f:
        f.write(key)
    return key


class Config:
    SECRET_KEY = _get_secret_key()
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 20,
    }
    OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY', '')
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production' or os.environ.get('FORCE_HTTPS') == 'true'
    SESSION_COOKIE_SAMESITE = 'Lax'
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024  # 1MB
