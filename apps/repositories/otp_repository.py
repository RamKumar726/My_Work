# apps/repositories/otp_repository.py
from apps import db
from utils import format_success_response  
from ..models.otp import Otp
from datetime import datetime, timedelta

def insert_new_otp_session(mobile_number, session_id, expiration_time):
    new_otp_session = Otp(mobile_number=mobile_number, otp=session_id, expiration_time=expiration_time)
    db.session.add(new_otp_session)
    db.session.commit()

def get_active_otp(mobile_number):
    otp =  Otp.query.filter_by(mobile_number=mobile_number, is_verified=0,status=1).first()
    print(otp)
    return otp

def is_otp_expired(otp_record):
    if otp_record.expiration_time < datetime.utcnow():
        db.session.delete(otp_record)
        db.session.commit()
        return True

def mark_otp_as_verified(otp_record):
    otp_record.is_verified = True
    db.session.commit()


def increment_failed_attempts(otp_record):
    otp_record.failed_attempts += 1
    db.session.commit()
    if otp_record.failed_attempts >= 5:
        return True

def update_otp_status(otp_record):
    otp_record.status = False
    db.session.commit()


