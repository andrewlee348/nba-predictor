from fastapi import FastAPI
import json
import os.path

app = FastAPI(
    title="nba_predictor_api"
)

@app.get("/predictions")
async def get_predictions():
    if os.path.isfile("./predictions/tod_pred.json"):
        f = open("./predictions/tod_pred.json")
        return json.load(f)
    else:
        return {"message": "Error: missing today's predictions"}

@app.get("/team_stats")
async def get_team_stats():
    if os.path.isfile("./teams/team_pred_stats.json"):
        f = open("./teams/team_pred_stats.json")
        return json.load(f)
    else:
        return {"message": "Error: missing team statistics"}