from utils import generate_jwt, generate_random_username, validate_otp
from ..repositories.otp_repository import get_active_otp, is_otp_expired, mark_otp_as_verified, increment_failed_attempts
from ..repositories.user_repository import get_user_by_mobile, register_new_user
from config import Config
import requests
from datetime import datetime
from error_codes import ErrorCodes
import pytz

IST = pytz.timezone('Asia/Kolkata')

def handle_verify_otp(data):
    mobile_number = data.get('mobile_number')
    otp_entered = data.get('otp')
    extras = data.get('extras')
    
    if not validate_otp(otp_entered):
        return {"status": ErrorCodes.INVALID_OTP.code, "message": "Invalid OTP"}
    
    otp_record = get_active_otp(mobile_number)
    if otp_record:
        if is_otp_expired(otp_record):
            return {"status": ErrorCodes.OTP_EXPIRED.code, "message": "OTP Expired , Request New One."}

        session_id = otp_record.SESSION_ID
        otp_verify_url = f"https://2factor.in/API/V1/{Config.API_2FA}/SMS/VERIFY/{session_id}/{otp_entered}"

        try:
            otp_verify_response = requests.get(otp_verify_url)
            otp_verify_data = otp_verify_response.json()

            if otp_verify_data['Status'] == 'Success':
                mark_otp_as_verified(otp_record)
                user = get_user_by_mobile(mobile_number)
                if not user:
                    username = generate_random_username()
                    new_user = register_new_user(username=username, mobile_number=mobile_number, is_mobile_verified=1)
                    user = new_user
                    token = generate_jwt(
                        partner_id=1001,
                        auth_type="signup",
                        device_id=extras.get('device_fingerprint'),
                        username=username,
                        auth_time=datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S'),  
                        user_id=user.USER_ID, 
                        mobile_number=user.MOBILE_NUMBER,
                    )
                else:
                    token = generate_jwt(
                        partner_id=1001,
                        auth_type="signup",
                        device_id=extras.get('device_fingerprint'),
                        username=username,
                        auth_time=datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S'),  
                        user_id=user.USER_ID, 
                        mobile_number=user.MOBILE_NUMBER
                    )

                
                return {"status": ErrorCodes.SUCCESS.code, "message": "OTP verified Successfully" , "token": token}
            elif increment_failed_attempts(otp_record):
                return {"status": ErrorCodes.OTP_EXPIRED.code, "message": "OTP Expired , Request New One."}



            return {"status": ErrorCodes.INVALID_OTP.code, "message": "Invalid OTP"}

        except requests.exceptions.RequestException as e:
            return {"status": ErrorCodes.API_REQUEST_FAILED.code, "message": f"OTP verification request failed: {e}"}

        except Exception as e:
            return{"status": ErrorCodes.INTERNAL_SERVER_ERROR.code, "message":f"Unexpected error: {e}" }

    return {"status": ErrorCodes.SESSION_NOT_FOUND.code , "message": "OTP session not found"}
