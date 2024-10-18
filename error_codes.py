from enum import Enum

class ErrorCodes(Enum):
    INVALID_MATCH_STATUS_CODE = 400  # Invalid match status code provided
    NO_MATCHES_FOUND = 404  # No matches found for the given criteria
    TOKEN_EXPIRED = 401  # Invalid or expired token
    API_REQUEST_FAILED = 503  # Failed to fetch data from the external API
    INTERNAL_SERVER_ERROR = 500  # Unexpected server error occurred
    SUCCESS = 200  # Success response
    INVALID_PHONE_NUMBER = 400  # Invalid phone number input
    INVALID_OTP = 400
    OTP_SEND_FAILED = 500  # Failed to send OTP
    UNAUTHORIZED = 401  # Unauthorized access (e.g., no valid token)
    OTP_EXPIRED = 401
    SESSION_NOT_FOUND = 404
    TOKEN_REVOKED = 403
    TOKEN_ABOUT_TO_EXPIRE = 2001
    TOKEN_SIGN_MATCHES = 2002
    def __init__(self, code):
        self.code = code

    @property
    def description(self):
        return {
            200: "Success.",
            400: "Invalid request or input.",
            401: "Token is invalid or expired. Please log in again.",
            404: "No matches found for the given criteria.",
            500: "Failed to send OTP or an unexpected error occurred on the server.",
            503: "Failed to fetch data from the external API.",
            403: "The token has been revoked. Please log in again.",
            2001: "Token Abour Expire, New Token Generated",
            2002: "Token expired but a new token has been issued"
        }.get(self.code, "Unknown error")
