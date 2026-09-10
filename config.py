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
    # 首次生成，写入文件并限制权限（仅当前用户可读写）
    key = secrets.token_hex(32)
    try:
        with open(key_file, 'w') as f:
            f.write(key)
    except OSError:
        # Serverless function bundles are read-only. Production should provide
        # SECRET_KEY, but an in-memory fallback keeps the function bootable.
        return key
    # 限制文件权限：Unix chmod 600；Windows 尝试用 win32security 或回退到仅当前用户
    try:
        if os.name != 'nt':
            os.chmod(key_file, 0o600)
        else:
            try:
                import win32security
                import win32con
                sd = win32security.GetFileSecurity(key_file, win32con.DACL_SECURITY_INFORMATION)
                dacl = win32security.ACL()
                user_sid = win32security.ConvertSidAccountName(
                    win32security.GetUserName(), win32con.SID_TYPE_USER
                )
                dacl.AddAccessAllowedAce(
                    win32security.ACL_REVISION,
                    win32con.FILE_GENERIC_READ | win32con.FILE_GENERIC_WRITE,
                    user_sid
                )
                sd.SetSecurityDescriptorDacl(1, dacl, 0)
                win32security.SetFileSecurity(key_file, win32con.DACL_SECURITY_INFORMATION, sd)
            except ImportError:
                # pywin32 不可用，使用简单文件属性限制
                import ctypes
                ctypes.windll.kernel32.SetFileAttributesW(key_file, 0x80)  # FILE_ATTRIBUTE_NORMAL
    except Exception:
        pass
    return key


def _get_database_url():
    """Use SQLAlchemy's modern psycopg driver for Render PostgreSQL URLs."""
    url = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3')
    if url.startswith('postgres://'):
        return 'postgresql+psycopg://' + url.removeprefix('postgres://')
    if url.startswith('postgresql://'):
        return 'postgresql+psycopg://' + url.removeprefix('postgresql://')
    return url


class Config:
    SECRET_KEY = _get_secret_key()
    SQLALCHEMY_DATABASE_URI = _get_database_url()
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
