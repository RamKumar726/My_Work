
from flask import Blueprint
import logging
from utils import format_success_response
from ..services.match_service import fetch_matches_data
from error_codes import ErrorCodes
from utils import check_token


fetch_matches_blueprint = Blueprint('fetch_matches',__name__)

@fetch_matches_blueprint.route('/fetch_matches/<int:code>', methods=['GET'])
def fetch_matches(code):
    token_check = check_token()
    if token_check[1] != 200:
        return format_success_response(token_check[1], token_check[0]), token_check[1]

    try:
        token_payload = token_check[0].get("payload")

        response  =  fetch_matches_data(code , token_payload)   
        status = response.get('status')
        data = response.get('matches') if  response.get('matches') else response.get('message')
        return {"data" : data ,"status": status }
    
    except Exception as e:
        logging.error(f"Error fetching matches: {e}")
        return {"message": ErrorCodes.INTERNAL_SERVER_ERROR.description, "status": ErrorCodes.INTERNAL_SERVER_ERROR.value}
