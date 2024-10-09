from ..models.user import User
from apps import db
def get_user_by_mobile(mobile_number):
    return User.query.filter_by(mobile_number=mobile_number).first()

def register_new_user(username,mobile_number,is_mobile_verified=1,agreed_to_terms=1):
    new_user =  User(username=username, mobile_number=mobile_number,is_mobile_verified=is_mobile_verified,agreed_to_terms=agreed_to_terms)
    db.session.add(new_user)
    db.session.commit()
    return new_user

