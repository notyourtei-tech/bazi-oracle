from models.user import db
from datetime import datetime
import json

class Chart(db.Model):
    __tablename__ = 'chart'
    __table_args__ = (
        db.Index('idx_chart_user_id', 'user_id'),
        db.Index('idx_chart_created_at', 'created_at'),
        db.Index('idx_chart_user_own', 'user_id', 'is_own'),
    )

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 输入参数
    name = db.Column(db.String(100))
    birth_country = db.Column(db.String(10))
    birth_date = db.Column(db.String(20))
    birth_time = db.Column(db.String(20))
    gender = db.Column(db.String(10))

    # 结果（JSON 存储）
    result_json = db.Column(db.Text)

    # 是否为用户自己的八字
    is_own = db.Column(db.Boolean, default=False)

    def get_result(self):
        if not self.result_json:
            return {}
        try:
            return json.loads(self.result_json)
        except (json.JSONDecodeError, TypeError):
            return {}
