from .user import db

class HistoryEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chart_id = db.Column(db.Integer, db.ForeignKey('chart.id'), nullable=False)
    year = db.Column(db.Integer)
    event_type = db.Column(db.String(30))
    description = db.Column(db.Text)
