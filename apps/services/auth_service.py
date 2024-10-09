from ..repositories.user_repository import get_user_by_mobile
from ..repositories.otp_repository import insert_new_otp_session

from utils import check_token, format_success_response, validate_phone_number, generate_jwt
from config import Config
import requests
import logging
from datetime import datetime


def handle_auth(data=None):
    # Check for the JWT token in headers
    response, status_code = check_token()
    if status_code == 201:
        token_payload = response.get("payload")
        # Fetch the user from the database using the phone_number from token payload
        user = get_user_by_mobile(token_payload.get('mobile_number'))
        # If token is valid and user exists, return success (auto-login)
        if user and token_payload['user_id'] == user.user_id:
            return format_success_response(200, {"success": "Token is valid, login successful"}), 200
        
    
    # If no token, token expired, or user not found, proceed with OTP flow
    if not data or 'mobile_number' not in data:
        return format_success_response(401, {"error": "Token expried, Please login"}), 401

    mobile_number = data.get('mobile_number')

    # Validate the phone number
    if not validate_phone_number(mobile_number):
        return format_success_response(400, {"error": "Invalid Phone Number"}), 400
    
    # Fetch the user based on phone number
    user = get_user_by_mobile(mobile_number)
    
    # Send OTP for login or signup
    otp_send_url = f"{Config.OTP_BASE_URL}/{Config.API_2FA}/SMS/{mobile_number}/AUTOGEN"
    
    try:
        otp_response = requests.get(otp_send_url)
        otp_data = otp_response.json()

        if otp_data['Status'] == 'Success':
            session_id = otp_data['Details']
            expiration_time = datetime.utcnow() + Config.OTP_EXPIRY_TIME
            insert_new_otp_session(mobile_number, session_id, expiration_time)
            
            if user:
                return format_success_response(200, {"success": "OTP sent for login"}), 200
            else:
                return format_success_response(200, {"success": "OTP sent for Sign Up"}), 200
            
        return format_success_response(500, {"error": "Failed to send OTP"}), 500

    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error while sending OTP: {e}")
        return format_success_response(500, {"error": "OTP service returned an error"}), 500

    except requests.exceptions.RequestException as e:
        logging.error(f"OTP service request failed: {e}")
        return format_success_response(500, {"error": "OTP service unavailable"}), 500

    except ValueError as e:
        logging.error(f"Failed to parse OTP service response: {e}")
        return format_success_response(500, {"error": "Invalid response from OTP service"}), 500

    except Exception as e:
        logging.error(f"Unexpected error during OTP generation: {e}")
        return format_success_response(500, {"error": "An unexpected error occurred"}), 500
