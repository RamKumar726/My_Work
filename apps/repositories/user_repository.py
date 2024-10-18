import pytz
from datetime import datetime
from ..models.user import User
from apps import db

IST = pytz.timezone('Asia/Kolkata')
def get_user_by_mobile(mobile_number):
    return User.query.filter_by(MOBILE_NUMBER=mobile_number).first()

def register_new_user(username,mobile_number,is_mobile_verified=1,agreed_to_terms=1):
    new_user =  User(USERNAME=username, MOBILE_NUMBER=mobile_number,IS_MOBILE_VERIFIED=is_mobile_verified,AGREED_TO_TERMS=agreed_to_terms)
    db.session.add(new_user)
    db.session.commit()
    return new_user

