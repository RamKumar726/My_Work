from ..repositories.user_repository import get_user_by_mobile
from ..repositories.otp_repository import insert_new_otp_session
from utils import check_token, regenerate_token
from config import Config
import requests
import logging
from datetime import datetime, timedelta
import pytz
from error_codes import ErrorCodes

IST = pytz.timezone('Asia/Kolkata')

def handle_auth(data=None):
    response, status_code = check_token()
    # Check for valid token
    if status_code == ErrorCodes.SUCCESS.code:
        token_payload = response.get("payload")
        user = get_user_by_mobile(token_payload.get('mobile_number'))
        
        # Validate user
        if user and token_payload['user_id'] == user.USER_ID and token_payload['mobile_number'] == user.MOBILE_NUMBER:
            return {"status": ErrorCodes.SUCCESS.code, "message": "Token is valid, login successful"}
    elif status_code == ErrorCodes.TOKEN_ABOUT_TO_EXPIRE.code:
        token_payload = response.get("payload")
        new_token = regenerate_token(token_payload)
        return {"status": ErrorCodes.SUCCESS.code, "message": "LoggedIn Successful" , "token": new_token}
    elif status_code == ErrorCodes.TOKEN_SIGN_MATCHES.code:
        return {"status": ErrorCodes.TOKEN_SIGN_MATCHES.code, "message":ErrorCodes.TOKEN_SIGN_MATCHES.description, "new_token": response.get('new_token')}

    elif status_code == ErrorCodes.TOKEN_REVOKED.code:
        return {"status": ErrorCodes.TOKEN_REVOKED , "message": ErrorCodes.TOKEN_REVOKED.description}


    
    # If no data or mobile number is provided, return token expired error
    if not data or 'mobile_number' not in data:
        return {"status": ErrorCodes.TOKEN_EXPIRED.code, "message": ErrorCodes.TOKEN_EXPIRED.description}

    mobile_number = data.get('mobile_number')
    
    # Validate phone number format
    if not isinstance(mobile_number, int) or not (1000000000 <= mobile_number <= 9999999999):
        return {"status": ErrorCodes.INVALID_PHONE_NUMBER.code, "message": ErrorCodes.INVALID_PHONE_NUMBER.description}

    # Prepare the OTP send request URL
    otp_send_url = f"{Config.OTP_BASE_URL}/{Config.API_2FA}/SMS/+91{mobile_number}/AUTOGEN"

    try:
        otp_response = requests.get(otp_send_url)
        otp_data = otp_response.json()
        
        # Check if OTP request was successful
        if otp_data['Status'] == 'Success':
            session_id = otp_data['Details']
            created_at = datetime.now(IST)
            expiration_time = created_at + timedelta(minutes=int(Config.OTP_EXPIRY_TIME))
            
            # Insert new OTP session in the database
            insert_new_otp_session(mobile_number, session_id, created_at, expiration_time)
            user = get_user_by_mobile(mobile_number)
            
            # Return success message based on user existence
            if user:
                return {"status": ErrorCodes.SUCCESS.code, "message": "OTP sent for login"}
            else:
                return {"status": ErrorCodes.SUCCESS.code, "message": "OTP sent for Sign Up"}
        
        # Handle OTP send failure
        return {"status": ErrorCodes.OTP_SEND_FAILED.code, "message": "Failed to send OTP."}

    except requests.exceptions.RequestException as e:
        logging.error(f"OTP service request failed: {e}")
        return {"status": ErrorCodes.API_REQUEST_FAILED.code, "message": ErrorCodes.API_REQUEST_FAILED.description}

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return {"status": ErrorCodes.INTERNAL_SERVER_ERROR.code, "message": ErrorCodes.INTERNAL_SERVER_ERROR.description}
