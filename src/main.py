import os
import requests

from dotenv import load_dotenv

from api.odds_client import get_odds
from utils.odds import (
    get_moneyline_market,
    normalize_probabilities,
)
from models.poisson import (
    estimate_lambdas,
    score_matrix,
)

load_dotenv()


def get_world_cup_matches():

    response = requests.get(
        "https://api.odds-api.io/v3/events",
        params={
            "apiKey": os.environ["ODDS_API_KEY"],
            "sport": "football",
            "status": "pending",
            "limit": 100,
        },
        timeout=10,
    )

    response.raise_for_status()

    events = response.json()

    return [
        event
        for event in events
        if "fifa-world-cup" in event["league"]["slug"]
    ]


def main():

    matches = get_world_cup_matches()

    if not matches:
        print("No World Cup matches found.")
        return

    print("\nUpcoming World Cup Matches\n")

    for index, match in enumerate(matches, start=1):
        print(
            f"{index}) "
            f"{match['home']} vs {match['away']}"
        )

    selection = int(input("\nSelect a match: "))

    selected_match = matches[selection - 1]

    event_id = selected_match["id"]

    print(
        f"\nSelected: "
        f"{selected_match['home']} vs {selected_match['away']}"
    )

    odds_data = get_odds(event_id)

    moneyline = get_moneyline_market(odds_data)

    home_odds = float(moneyline["home"])
    draw_odds = float(moneyline["draw"])
    away_odds = float(moneyline["away"])

    probabilities = normalize_probabilities(
        home_odds,
        draw_odds,
        away_odds,
    )

    home_lambda, away_lambda = estimate_lambdas(
        probabilities["home"],
        probabilities["away"],
    )

    scores = score_matrix(
        home_lambda,
        away_lambda,
    )

    print("\nMarket Probabilities")
    print("--------------------")
    print(
        f"{selected_match['home']}: "
        f"{probabilities['home'] * 100:.2f}%"
    )
    print(
        f"Draw: "
        f"{probabilities['draw'] * 100:.2f}%"
    )
    print(
        f"{selected_match['away']}: "
        f"{probabilities['away'] * 100:.2f}%"
    )

    print("\nExpected Goals")
    print("--------------")
    print(
        f"{selected_match['home']}: "
        f"{home_lambda:.2f}"
    )
    print(
        f"{selected_match['away']}: "
        f"{away_lambda:.2f}"
    )

    print("\nTop 10 Predicted Scores")
    print("-----------------------")

    for score, probability in scores[:10]:
        print(
            f"{score:<5} "
            f"{probability * 100:.2f}%"
        )


if __name__ == "__main__":
    main()