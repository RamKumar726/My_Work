from config import Config

from ..repositories.match_format_repository import  get_match_formats_list
from ..repositories.category_type_repository import get_category_type_list
import requests

status_mapping = {
    1: 'Scheduled',
    2: 'Completed',
    3: 'Live',
    4: 'Abandoned'
}

def fetch_matches_data(status_code, token):
    response = requests.get(f'{Config.ENTITY_API_URL}/?token={Config.ENTITY_API_KEY}', headers={'Authorization': f'Bearer {token}'})
    
    if response.status_code == 200:
        data = response.json()
        items = data.get('response', {}).get('items', [])
        
        category_type_list = get_category_type_list()
        match_formats_list = get_match_formats_list()

        filtered_matches = [match for match in items if match.get('status') == status_code]
        if len(filtered_matches) == 0:
            return {'message': f"There are no {status_mapping.get(status_code, 'matches for this status code')} Matches"}, 404

        if status_code == 1:
            return _process_scheduled_matches(filtered_matches, category_type_list, match_formats_list)
        elif status_code == 3:
            return _process_live_matches(filtered_matches, category_type_list, match_formats_list)

        return filtered_matches

    elif response.status_code == 401:
        raise Exception("Token is invalid or expired. Please refresh.")
    else:
        raise Exception("Failed to fetch data from API")

def _process_scheduled_matches(matches, category_type_list, match_formats_list):
    scheduled_matches = {
        "status": "success",
        "matches": {
            "1": [],  # ODI matches will go here
            "2": [],  # Test matches will go here
            "3": [],  # T20 matches will go here
        }
    }


    # Loop through each match only once
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

        return {"status": "success", "live_matches": scheduled_matches}
    


def _process_live_matches(matches, category_type_list, match_formats_list):
    live_matches = {
        "status": "success",
        "matches": {
            "1": [],  # ODI matches will go here
            "2": [],  # Test matches will go here
            "3": [],  # T20 matches will go here
        }
    }


    # Loop through each match only once
    for match in matches:
        category = match.get('competition', {}).get('category', 'Unknown').lower()
        match_format = match.get("format_str", "Unknown")

        if category in category_type_list and  match_format.lower() in match_formats_list:
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
                "trades_placed": 100,  #assume as 100
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

                
    return {"status": "success", "live_matches": live_matches}

