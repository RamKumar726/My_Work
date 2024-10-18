# apps/repositories/otp_repository.py
from apps import db
from ..models.otp import Otp
import pytz
from datetime import datetime, timezone

IST  = pytz.timezone('Asia/Kolkata')

def insert_new_otp_session(mobile_number, session_id,created_at, expiration_time):
    new_otp_session = Otp(MOBILE_NUMBER=mobile_number, SESSION_ID=session_id, CREATED_AT =created_at, EXPIRATION_TIME = expiration_time)
    db.session.add(new_otp_session)
    db.session.commit()

def get_active_otp(mobile_number):
    otp =  Otp.query.filter_by(MOBILE_NUMBER=mobile_number, IS_VERIFIED=0,STATUS=1).first()
    return otp

def is_otp_expired(otp_record):
    expiration_time_aware = otp_record.EXPIRATION_TIME.replace(tzinfo=pytz.utc).astimezone(IST)
    if expiration_time_aware <datetime.now(IST):
        otp_record.STATUS = 0
        db.session.commit()
        return True

def mark_otp_as_verified(otp_record):
    otp_record.IS_VERIFIED = 1
    otp_record.STATUS = 0
    db.session.commit()


def increment_failed_attempts(otp_record):
    otp_record.FAILED_ATTEMPTS += 1
    db.session.commit()
    if otp_record.FAILED_ATTEMPTS >= 5:
        otp_record.STATUS = 0
        db.session.commit()
        return True

def update_otp_status(otp_record):
    otp_record.STATUS = 0
    db.session.commit()


