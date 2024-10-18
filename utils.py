import logging
from flask import request
import random
import string
import datetime
import jwt
import re
from config import Config
import pytz
from error_codes import ErrorCodes
import uuid
from redis import Redis


import jwt
import datetime


# redis_client = Redis()
IST = pytz.timezone('Asia/Kolkata')
def generate_jwt(partner_id, auth_type, device_id, username,auth_time,iat,user_id,mobile_number,exp,jti):
    now_ist = datetime.datetime.now(IST)
    expiration_days = int(Config.JWT_EXPIRATION_TIME) if Config.JWT_EXPIRATION_TIME else 7  # Default to 7 days
    payload = {
        'partner_id': partner_id,
        'auth_type': auth_type,
        'device_id': device_id,
        'username': username,
        'iss': Config.API_DOMAIN,
        'aud': Config.BRAND_NAME,
        'auth_time': auth_time,
        'iat': now_ist.timestamp(),
        'user_id': user_id,
        'mobile_number': mobile_number,
        'exp':( now_ist + datetime.timedelta(days=expiration_days)).timestamp(), # Set expiration
        'jti' : str(uuid.uuid4())
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
    return token



def generate_random_username(length=10):
    characters = string.ascii_letters + string.digits  # Contains letters and digits
    username = ''.join(random.choice(characters) for _ in range(length))
    return username



def validate_otp(otp):
    # Validates the OTP to ensure it is exactly 6 digits.
    return len(otp) == 6 and otp.isdigit()

def check_token():
    token = request.headers.get('Authorization')  # Retrieve token from headers
    if not token or not token.startswith('Bearer '):
        return {
            "status": ErrorCodes.UNAUTHORIZED.code,
            "message": ErrorCodes.UNAUTHORIZED.description
        }
    
    try:
        # Strip 'Bearer ' from the token
        token = token.split(' ')[1]
     
        # Decode the token and return the payload if valid
        decoded = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'], audience='opinion')
    
        jti = decoded.get('jti')

        # if redis_client.exists(jti):
        #     return{
        #         "status": ErrorCodes.TOKEN_REVOKED.code,
        #         "message": ErrorCodes.TOKEN_REVOKED.description
        #     }
        exp = datetime.datetime.fromtimestamp(decoded['exp']).timestamp()

        now = (datetime.datetime.now(IST)).timestamp()
        if exp > now + 300:
            return {"status": "success", "payload": decoded}, ErrorCodes.SUCCESS.code
        # Token is valid but about to expire
        elif exp < now+300:
            return {
                "status": ErrorCodes.TOKEN_ABOUT_TO_EXPIRE.code,
                "message": ErrorCodes.TOKEN_ABOUT_TO_EXPIRE.description,
                "payload": decoded
            }, ErrorCodes.TOKEN_ABOUT_TO_EXPIRE.code
        

    
    except jwt.ExpiredSignatureError:
        # If token has expired but the signature matches, generate a new token
        try:
            # Decode the token without verifying expiration
            decoded = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'], audience=Config.BRAND_NAME, options={"verify_exp": False})
            
            # Generate a new token
            new_token = regenerate_token(decoded)
            
            return {
                "status": ErrorCodes.TOKEN_SIGN_MATCHES.code,
                "message": "Token expired but a new token has been issued.",
                "new_token": new_token
            }, ErrorCodes.TOKEN_SIGN_MATCHES.code
        
        except jwt.InvalidTokenError as e:
            logging.error(f"Invalid token error while renewing: {str(e)}")
            return {
                "status": ErrorCodes.UNAUTHORIZED.code,
                "message": "Failed to regenerate token."
            }, ErrorCodes.UNAUTHORIZED.code
    
    except jwt.InvalidTokenError as e:
        # Log the specific error for debugging
        logging.error(f"Invalid token error: {str(e)}")
        return {
            "status": ErrorCodes.UNAUTHORIZED.code,
            "message": ErrorCodes.UNAUTHORIZED.description
        }, ErrorCodes.UNAUTHORIZED.code



def regenerate_token(decoded):
    jti = decoded.get('jti')
    auth_time = decoded.get('auth_time')
    partner_id = decoded.get('partner_id')
    auth_type = 'login'
    device_id = decoded.get('device_id')
    username = decoded.get('username')
    auth_time = decoded.get('auth_time')
    user_id = decoded.get('auth_time')
    mobile_number = decoded.get('mobile_number')
    iat = datetime.datetime.now(IST).timestamp()
    exp = (datetime.datetime.now(IST)+datetime.timedelta(hours=1)).timestamp()
    new_token = generate_jwt(
        partner_id=partner_id,
        auth_type=auth_type,
        device_id=device_id,
        username=username,
        auth_time=auth_time,
        iat=iat,
        user_id=user_id,
        mobile_number=mobile_number,
        exp=exp,
        jti=jti
    )
    return new_token