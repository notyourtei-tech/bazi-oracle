from .user import db

class HistoryEvent(db.Model):
    __tablename__ = 'history_event'
    __table_args__ = (
        db.Index('idx_he_chart_id', 'chart_id'),
        db.Index('idx_he_year', 'year'),
    )

    id = db.Column(db.Integer, primary_key=True)
    chart_id = db.Column(db.Integer, db.ForeignKey('chart.id'), nullable=False)
    year = db.Column(db.Integer)
    event_type = db.Column(db.String(30))
    description = db.Column(db.Text)
