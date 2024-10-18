from datetime import datetime
import pytz
from apps import db

# Define IST timezone
IST = pytz.timezone('Asia/Kolkata')

class User(db.Model):
    __tablename__ = 'user'

    USER_ID = db.Column(db.BigInteger, primary_key=True)
    REFFERER_ID = db.Column(db.BigInteger, nullable=True)
    MOBILE_NUMBER = db.Column(db.BigInteger, unique=True, nullable=True)
    USERNAME = db.Column(db.String(50), unique=True, nullable=True)
    FULL_NAME = db.Column(db.String(50), nullable=True)
    DOB = db.Column(db.Date, nullable=True)
    GENDER = db.Column(db.String(10), nullable=True)
    EMAIL = db.Column(db.String(100), nullable=True)
    PROFILE_PICTURE = db.Column(db.String(255), nullable=True)
    STATE = db.Column(db.String(255), nullable=True)
    ADDRESS = db.Column(db.String(1000), nullable=True)
    COUNTRY = db.Column(db.String(1000), nullable=True)
    IS_EMAIL_VERIFIED = db.Column(db.Boolean, default=False)
    AGREED_TO_TERMS = db.Column(db.Boolean, default=False)
    IS_KYC_VERIFIED = db.Column(db.Boolean, default=False)
    IS_MOBILE_VERIFIED = db.Column(db.Boolean, default=False)
    USER_LEVEL_ID = db.Column(db.BigInteger, nullable=True)
    LAST_LOGINED = db.Column(db.DateTime, nullable=True)
    USER_STATUS = db.Column(db.Boolean, default=True)

    # Use IST timezone for created and updated date
    CREATED_DATE = db.Column(db.DateTime, default=lambda:datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S'))
    UPDATED_DATE = db.Column(db.DateTime, default=lambda: datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S'), onupdate=lambda: datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S'))

    def __repr__(self):
        return f'<User {self.USERNAME} Mobile_number {self.MOBILE_NUMBER}>'
