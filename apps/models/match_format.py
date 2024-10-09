from datetime import datetime
from apps import db

class MatchFormat(db.Model):
    __tablename__ = 'match_formats'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    type = db.Column(db.String(255), nullable=True, comment='ODI, TEST, T20, T10')
    overs = db.Column(db.SmallInteger, nullable=True)
    description = db.Column(db.String(255), nullable=True)
    status = db.Column(db.SmallInteger, nullable=True)  # 1 for active, 0 for inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<MatchFormat {self.type} - Status: {self.status}>'
