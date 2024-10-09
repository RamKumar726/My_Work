
from flask import Blueprint
import logging
from utils import format_success_response
from ..services.match_service import fetch_matches_data

from utils import check_token


fetch_matches_blueprint = Blueprint('fetch_matches',__name__)

@fetch_matches_blueprint.route('/fetch_matches/<int:code>', methods=['GET'])
def fetch_matches(code):
    token_check = check_token()

    if token_check[1] != 201:
        return format_success_response("error", token_check[0]), token_check[1]

    try:
        token_payload = token_check[0].get("payload")
        data = fetch_matches_data(code, token_payload)
        return format_success_response("success", data), 200
    except Exception as e:
        logging.error(f"Error fetching matches: {e}")
        return format_success_response("error", {"message": "An error occurred while fetching matches"}), 500
