from config import Config
from ..repositories.match_format_repository import get_match_formats_list
from ..repositories.category_type_repository import get_category_type_list
from error_codes import ErrorCodes  # Import the updated error codes
import requests

status_mapping = {
    1: 'Scheduled',
    3: 'Live',
}

def fetch_matches_data(match_status_code, token):
    try:
        # Validate the match status code
        if match_status_code not in status_mapping:
            return {"message": ErrorCodes.INVALID_MATCH_STATUS_CODE.description, "status": ErrorCodes.INVALID_MATCH_STATUS_CODE.value}

        response = requests.get(f'{Config.ENTITY_API_URL}/?token={Config.ENTITY_API_KEY}', headers={'Authorization': f'Bearer {token}'})
        if response.status_code == 200:
            data = response.json()
            items = data.get('response', {}).get('items', [])

            category_type_list = get_category_type_list()
            match_formats_list = get_match_formats_list()

            # Filter matches by status code
            filtered_matches = [match for match in items if match.get('status') == match_status_code]

            # Handle case when no matches are found
            if not filtered_matches:
                return {"message": ErrorCodes.NO_MATCHES_FOUND.description, "status": ErrorCodes.NO_MATCHES_FOUND.value}

            # Process matches based on status code (Scheduled or Live)
            if match_status_code == 1:
                return _process_scheduled_matches(filtered_matches, category_type_list, match_formats_list)
            elif match_status_code == 3:
                return _process_live_matches(filtered_matches, category_type_list, match_formats_list)
            else:
                return {"message": ErrorCodes.INVALID_MATCH_STATUS_CODE.description, "status": ErrorCodes.INVALID_MATCH_STATUS_CODE.value}

        elif response.status_code == 401:
            return {"message": ErrorCodes.TOKEN_EXPIRED.description, "status": ErrorCodes.TOKEN_EXPIRED.value}
        else:
            return {"message": ErrorCodes.API_REQUEST_FAILED.description, "status": response.status_code}

    except Exception as e:
        return {"message": ErrorCodes.INTERNAL_SERVER_ERROR.description, "status": ErrorCodes.INTERNAL_SERVER_ERROR.value}


def _process_scheduled_matches(matches, category_type_list, match_formats_list):
    scheduled_matches = {
        "status": 200,
        "matches": {
            "1": [],  # ODI matches
            "2": [],  # Test matches
            "3": [],  # T20 matches
        }
    }
    for match in matches:
        category = match.get('competition', {}).get('category', 'Unknown').lower()
        match_format = match.get("format_str", "Unknown")
        
        if category in category_type_list and match_format.lower() in match_formats_list:
            match_data = {
                "title": match["title"],
                "match_id": match["match_id"],
                "short_title": match["short_title"],
                "subtitle": match["subtitle"],
                "match_number": match["match_number"],
                "date_start": match["date_start"].split(" ")[0],
                "time_start": match['date_start'].split(" ")[1],
                "format_str": match_format,
                "live": match.get("live", False),
                "result": match["result"],
                "trades_placed": 100,  # Assume as 100
                "teama": {
                    "team_id": match["teama"].get("team_id"),
                    "name": match["teama"].get("name"),
                    "short_name": match["teama"].get("short_name"),
                    "logo_url": match["teama"].get("logo_url")
                },
                "teamb": {
                    "team_id": match["teamb"].get("team_id"),
                    "name": match["teamb"].get("name"),
                    "short_name": match["teamb"].get("short_name"),
                    "logo_url": match["teamb"].get("logo_url")
                }
            }

            if match_format == "ODI":
                scheduled_matches["matches"]["1"].append(match_data)
            elif match_format == "Test":
                scheduled_matches["matches"]["2"].append(match_data)
            elif match_format == "T20I":
                scheduled_matches["matches"]["3"].append(match_data)
    
    return scheduled_matches


def _process_live_matches(matches, category_type_list, match_formats_list):
    live_matches = {
        "status": 200,
        "matches": {
            "1": [],  # ODI matches
            "2": [],  # Test matches
            "3": [],  # T20 matches
        }
    }

    for match in matches:
        category = match.get('competition', {}).get('category', 'Unknown').lower()
        match_format = match.get("format_str", "Unknown")
        decision = match.get('toss', {}).get('decision')
        toss_winner = match.get("toss", {}).get('winner')
        latest_inning_number = match.get('latest_inning_number')
        teama = match.get('teama', {})
        teamb = match.get('teamb', {})

        score_card = "Match Not Started Yet"
        if decision == 1:
            score_card = teama['scores_full'] if latest_inning_number == 1 and teama['team_id'] == toss_winner else teamb['scores_full']
        elif decision == 2:
            score_card = teamb['scores_full'] if latest_inning_number == 1 and teama['team_id'] == toss_winner else teama['scores_full']

        if category in category_type_list and match_format.lower() in match_formats_list:
            match_data = {
                "title": match["title"],
                "match_id": match["match_id"],
                "short_title": match["short_title"],
                "subtitle": match["subtitle"],
                "match_number": match["match_number"],
                "date_start": match["date_start"].split(" ")[0],
                "time_start": match['date_start'].split(" ")[1],
                "format_str": match_format,
                "live": match.get("live", True),
                "result": match["result"],
                "trades_placed": 100,  # Assume as 100
                "score_card": score_card,
                "teama": {
                    "team_id": match["teama"].get("team_id"),
                    "name": match["teama"].get("name"),
                    "short_name": match["teama"].get("short_name"),
                    "logo_url": match["teama"].get("logo_url")
                },
                "teamb": {
                    "team_id": match["teamb"].get("team_id"),
                    "name": match["teamb"].get("name"),
                    "short_name": match["teamb"].get("short_name"),
                    "logo_url": match["teamb"].get("logo_url")
                }
            }

            if match_format == "ODI":
                live_matches["matches"]["1"].append(match_data)
            elif match_format == "Test":
                live_matches["matches"]["2"].append(match_data)
            elif match_format == "T20I":
                live_matches["matches"]["3"].append(match_data)
    
    return live_matches
