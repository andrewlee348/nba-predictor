from datetime import datetime
import json

from nba_api.stats.endpoints import leaguedashteamstats

def flush_team_pred_stats():
    try:
        ldts = leaguedashteamstats.LeagueDashTeamStats().get_dict().get("resultSets")[0]
        all_pred_stats = {}
        for row in ldts.get("rowSet"):
            pred_stats = {}

            pred_stats["TEAM_NAME"] = row[1]
            pred_stats["FG%"] = row[9]
            pred_stats["FT%"] = row[15]
            pred_stats["3P%"] = row[12]
            pred_stats["OREB"] = round(row[16]/row[2], 2)
            pred_stats["FTA"] = round(row[14]/row[2], 2)
            pred_stats["TOV"] = round(row[20]/row[2], 2)
            pred_stats["AST"] = round(row[19]/row[2], 2)
            pred_stats["NET_RTG"] = round(row[27]/row[2], 2)

            all_pred_stats[row[0]] = pred_stats

        if pred_stats is not None:
            all_pred_stats["dateUpdated"] = str(datetime.utcnow())
            f = open("team_pred_stats.json", "w")
            f.write(json.dumps(all_pred_stats))
            f.close()
    except Exception as err:
        print(f'Exception: {err}')

flush_team_pred_stats()