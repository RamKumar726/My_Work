# apps/controllers/auth_controller.py
from flask import Blueprint, request, jsonify

auth_blurprint = Blueprint('auth', __name__)

@auth_blurprint.route('/auth', methods=['POST'])
def auth():
    from ..services.auth_service import handle_auth
    data = request.json
    return handle_auth(data)

verify_otp_blueprint =  Blueprint('verify_otp',__name__)


@verify_otp_blueprint.route("/verify_otp", methods= ['POST'])
def verify_otp():
    data  = request.get_json()
    from ..services.otp_service import handle_verify_otp
    return handle_verify_otp(data)