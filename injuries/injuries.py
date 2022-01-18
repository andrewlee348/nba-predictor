import requests
from requests.exceptions import HTTPError
from datetime import datetime
import json

from nba_api.stats.static import players
import team_name_mapping

ESPN_INJURIES_URL = "http://site.api.espn.com/apis/site/v2/sports/basketball/nba/injuries"

def get_full_injury_report():
    url = ESPN_INJURIES_URL
    response = requests.get(url)
    response.raise_for_status()
    return response.json().get("injuries")

def flush_injuries_by_team():
    try:
        full_injury_report = get_full_injury_report()
        for team in full_injury_report:
            team_injuries = {
                "name": team.get("displayName"),
                "injuries": []
            }
            for player in team.get("injuries"):
                player_info = player.get("athlete")
                player_name = player_info.get("displayName")
                player_injury = {
                    "full_name": player_name,
                    "shortComment": player.get("shortComment"),
                    "longComment": player.get("longComment"),
                    "dateUpdated": player.get("date"),
                    "details": player.get("details")
                }
                player_search = players.find_players_by_full_name(player_name)
                if player_search is not None and len(player_search) != 0:
                    player_injury["player_id"] = player_search[0].get("id")
                team_injuries.get("injuries").append(player_injury)
            if team_injuries.get("injuries") is not None:
                team_injuries["dateUpdated"] = str(datetime.utcnow())
                team_name_abb = team_name_mapping.abb.get(team_injuries.get("name"))
                f = open("by_team/" + team_name_abb + "_injuries.json", "w")
                f.write(json.dumps(team_injuries))
                f.close()
    except HTTPError as http_err:
        print(f'HTTP error: {http_err}')
    except Exception as err:
        print(f'Exception: {err}')

flush_injuries_by_team()
