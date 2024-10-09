import logging
from flask import request
import random
import string
from datetime import datetime
import jwt
import re
from config import Config





import jwt
import datetime

def generate_jwt(user_id, mobile_number):
    payload = {
        'user_id': user_id,
        'mobile_number': mobile_number,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)  # Set expiration
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
    return token



def generate_random_username(length=10):
    characters = string.ascii_letters + string.digits  # Contains letters and digits
    username = ''.join(random.choice(characters) for _ in range(length))
    return username



def validate_phone_number(phone_number):
    # Validates the phone number to ensure it is exactly 10 digits.
    pattern = re.compile(r'^\+91\d{10}$')
    return bool(pattern.match(phone_number))

def validate_otp(otp):
    # Validates the OTP to ensure it is exactly 6 digits.
    return len(otp) == 6 and otp.isdigit()


def check_token():
    token = request.headers.get('Authorization')  # Retrieve token from headers
    
    if not token or not token.startswith('Bearer '):
        return {"status": "error", "message": "Token is missing or malformed"}, 401
    
    try:
        # Strip 'Bearer ' from the token
        token = token.split(' ')[1]

        # Decode the token and return the payload if valid
        decoded = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        return {"status": "success", "payload": decoded}, 201
    
    except jwt.ExpiredSignatureError:
        # Token has expired, user must log in again
        return {
            "status": "error",
            "message": "Token expired, please log in again"
        }, 403
    
    except jwt.InvalidTokenError as e:
        # Log the specific error for debugging
        logging.error(f"Invalid token error: {str(e)}")
        return {"status": "error", "message": "Invalid token"}, 401



def format_success_response(code, data):
    return {
        'status': code,
        'data':data
    }