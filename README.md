# nba-predictor
NBA game outcome predictor using points spread and points differential between two teams on a given night

Models taken from: [Predicting Outcomes Of NBA Basketball Games by Eric Scot Jones](https://library.ndsu.edu/ir/bitstream/handle/10365/28084/Predicting%20Outcomes%20of%20NBA%20Basketball%20Games.pdf?sequence=1&isAllowed=y)

This project was designed with periodic flushes in mind.
Ideally, both gathering of statistics and prediction operations would run every 24 hours, or some other optimal period of time.

## Installation

In the root directory:
```
pip install -r requirements.txt
```

In teams directory, run:
```
python team_pred_stats.py
```

Then, in predictions directory, run:
```
python make_pred.py
```

To run the API server:
```
python -m uvicorn main:app --reload
```

You should now be able to access the API and its docs from http://localhost:8000/docs
