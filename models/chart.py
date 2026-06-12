from models.user import db
from datetime import datetime
import json

class Chart(db.Model):
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

    def get_result(self):
        return json.loads(self.result_json)
