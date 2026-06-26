from models.user import db
from datetime import datetime, timezone
import json
import gzip
import base64

class Chart(db.Model):
    __tablename__ = 'chart'
    __table_args__ = (
        db.Index('idx_chart_user_id', 'user_id'),
        db.Index('idx_chart_created_at', 'created_at'),
        db.Index('idx_chart_user_own', 'user_id', 'is_own'),
    )

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # 输入参数
    name = db.Column(db.String(100))
    birth_country = db.Column(db.String(10))
    birth_date = db.Column(db.String(20))
    birth_time = db.Column(db.String(20))
    gender = db.Column(db.String(10))

    # 结果（gzip 压缩 + base64 编码存储）
    result_json = db.Column(db.Text)

    # 是否为用户自己的八字
    is_own = db.Column(db.Boolean, default=False)

    def set_result(self, data):
        """压缩并存储结果 JSON"""
        raw = json.dumps(data, ensure_ascii=False).encode('utf-8')
        compressed = gzip.compress(raw, compresslevel=6)
        self.result_json = base64.b64encode(compressed).decode('ascii')

    def get_result(self):
        """读取并解压结果 JSON"""
        if not self.result_json:
            return {}
        try:
            decoded = base64.b64decode(self.result_json)
            raw = gzip.decompress(decoded)
            return json.loads(raw)
        except Exception:
            # 兼容旧的未压缩数据
            try:
                return json.loads(self.result_json)
            except (json.JSONDecodeError, TypeError):
                return {}
