def get_moneyline_market(odds_data):
    bet365_markets = odds_data["bookmakers"]["Bet365"]

    for market in bet365_markets:
        if market["name"] == "ML":
            return market["odds"][0]

    raise ValueError("Moneyline market not found")


def normalize_probabilities(home, draw, away):
    probs = [
        1 / home,
        1 / draw,
        1 / away,
    ]

    total = sum(probs)

    return {
        "home": probs[0] / total,
        "draw": probs[1] / total,
        "away": probs[2] / total,
    }