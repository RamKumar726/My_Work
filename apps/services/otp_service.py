from utils import validate_otp, format_success_response
from ..repositories.otp_repository import get_active_otp, is_otp_expired, mark_otp_as_verified, increment_failed_attempts, update_otp_status
from ..repositories.user_repository import get_user_by_mobile, register_new_user
from config import Config
from utils import generate_random_username, generate_jwt
import requests
import logging

def handle_verify_otp(data):
    mobile_number = data.get('mobile_number')
    otp_entered = data.get('otp')
    
    if not validate_otp(otp_entered):
        return format_success_response(400, {"error": "Invalid OTP format"}), 400
    otp_record = get_active_otp(mobile_number)

    if otp_record:
        if is_otp_expired(otp_record):
            update_otp_status(otp_record)
            return format_success_response(401, {"error": "OTP expired, request a new one"}), 401
        
        session_id = otp_record.otp
        otp_verify_url = f"https://2factor.in/API/V1/{Config.API_2FA}/SMS/VERIFY/{session_id}/{otp_entered}"

        try:
            otp_verify_response = requests.get(otp_verify_url)
            otp_verify_data = otp_verify_response.json()

            if otp_verify_data['Status'] == 'Success':
                mark_otp_as_verified(otp_record)

                user = get_user_by_mobile(mobile_number)

                if not user:
                    username = generate_random_username()
                    new_user = register_new_user(username=username, mobile_number=mobile_number, is_mobile_verified=1,agreed_to_terms=1)
                    user = new_user


                token = generate_jwt(user.user_id, user.mobile_number)
                return format_success_response(200, {"success": "OTP verified successfully", "token": token}), 200
            elif increment_failed_attempts(otp_record):
                # If OTP entry attempts exceed the limit, prompt the user to request a new OTP
                update_otp_status(otp_record)
                return format_success_response(401, {"error": "You've entered the wrong OTP 5 times. Please request a new OTP."}), 401
                
            return format_success_response(400, {"error": "Invalid OTP"}), 400

        except requests.exceptions.RequestException as e:
            logging.error(f"OTP verification request failed: {e}")
            return format_success_response(500, {"error": "OTP verification service unavailable"}), 500

        except Exception as e:
            logging.error(f"Unexpected error during OTP verification: {e}")
            return format_success_response(500, {"error": "An unexpected error occurred"}), 500

    return format_success_response(401, {"error": "OTP session not found, Request New one"}), 401