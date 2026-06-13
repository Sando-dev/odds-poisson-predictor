import os
import requests


BASE_URL = "https://api.odds-api.io/v3/odds"


def get_odds(event_id: int):
    response = requests.get(
        BASE_URL,
        params={
            "apiKey": os.environ["ODDS_API_KEY"],
            "eventId": event_id,
            "bookmakers": "Bet365,Unibet",
        },
        timeout=10,
    )

    response.raise_for_status()

    return response.json()