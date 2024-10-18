from datetime import datetime, timedelta
from app import db

class Otp(db.Model):
    __tablename__ = 'OTP_TRACKING'
    
    ID = db.Column(db.BigInteger, primary_key=True)  # Use BigInteger for consistency with MySQL
    MOBILE_NUMBER = db.Column(db.BigInteger, nullable=False)  # Use BigInteger for mobile number
    SESSION_ID = db.Column(db.String(100), nullable=False)
    CREATED_AT = db.Column(db.DateTime)  # Default to current UTC time
    EXPIRATION_TIME = db.Column(db.DateTime)  # OTP expires in 5 minutes
    FAILED_ATTEMPTS = db.Column(db.Integer, default=0)  # Track failed attempts
    IS_VERIFIED = db.Column(db.Boolean, default=False)
    STATUS = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<OTP for {self.MOBILE_NUMBER}>'
