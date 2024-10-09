from datetime import datetime
from apps import db

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    mobile_number = db.Column(db.String(15), unique=True, nullable=False)
    is_mobile_verified =  db.Column(db.Boolean, default=False)
    agreed_to_terms = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'
