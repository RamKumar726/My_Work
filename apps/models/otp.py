from datetime import datetime, timedelta
from app import db

class Otp(db.Model):
    __tablename__ = 'otps'
    id = db.Column(db.Integer, primary_key=True)
    mobile_number = db.Column(db.String(15), nullable=False)  # Ensuring unique phone number
    otp = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expiration_time = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=5))  # OTP expires in 5 minutes
    failed_attempts = db.Column(db.Integer, default=0)  # Track failed attempts
    is_verified = db.Column(db.Boolean, default=False)
    status = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<OTP {self.otp} for {self.mobile_number}>'
