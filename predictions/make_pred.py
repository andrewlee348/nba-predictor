from datetime import datetime
import json

from nba_api.stats.endpoints import scoreboardv2
from nba_api.stats.static import teams

TODAY_DATE = datetime.today().strftime('%Y-%m-%d')

def calculate_diff(team_1, team_2):
    FGS = team_1.get("FG%") - team_2.get("FG%")
    FTS = team_1.get("FT%") - team_2.get("FT%")
    THREEPS = team_1.get("3P%") - team_2.get("3P%")
    ORS = team_1.get("OREB") - team_2.get("OREB")
    FTA = team_1.get("FTA") - team_2.get("FTA")
    TOS = team_1.get("TOV") - team_2.get("TOV")
    AST = team_1.get("AST") - team_2.get("AST")
    PTS_DIFF = team_1.get("NET_RTG") - team_2.get("NET_RTG")

    result = {
        "point_spread": 1.485*FGS*100 + 0.169*THREEPS*100 + 0.195*FTS*100 + 0.879*ORS + 0.337*FTA + 0.239*AST - 0.837*TOS,
        "points_diff": PTS_DIFF
    }

    return result

def flush_predictions():
    try:
        f = open("../teams/team_pred_stats.json")
        pred_stats = json.load(f)
        todays_games = scoreboardv2.ScoreboardV2(game_date=TODAY_DATE).get_dict().get("resultSets")[0]

        tod_pred = []

        for game in todays_games.get("rowSet"):
            game_id = game[2]
            team_1_id = game[6]
            team_2_id = game[7]

            team_1_stats = pred_stats.get(str(team_1_id))
            team_2_stats = pred_stats.get(str(team_2_id))

            diff_calc = calculate_diff(team_1_stats, team_2_stats)
        
            point_spread = diff_calc.get("point_spread")
            points_diff = diff_calc.get("points_diff")

            weighted_model = 0.7 * point_spread + 0.3 * points_diff

            winner = teams.find_team_name_by_id(team_1_id)

            if weighted_model < 0:
                winner = teams.find_team_name_by_id(team_2_id)
            
            game_pred = {
                "game_id": game_id,
                "winner_team_name": winner.get("full_name"),
                "winner_team_id": winner.get("id")
            }

            tod_pred.append(game_pred)

        f = open("tod_pred.json", "w")
        f.write(json.dumps(tod_pred))
        f.close()
    except Exception as err:
        print(f'Exception: {err}')
