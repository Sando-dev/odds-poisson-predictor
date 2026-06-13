from math import exp
from math import factorial


def poisson(k: int, lam: float) -> float:
    return (lam**k * exp(-lam)) / factorial(k)


def estimate_lambdas(home_prob: float, away_prob: float):
    """
    Estima goles esperados a partir de las probabilidades
    implícitas del mercado.

    MVP simple:
    - Total de goles esperado fijo.
    - Repartido según la fuerza relativa de cada equipo.
    """

    total_goals = 2.2

    strength = home_prob + away_prob

    home_lambda = total_goals * home_prob / strength
    away_lambda = total_goals * away_prob / strength

    return home_lambda, away_lambda


def score_matrix(home_lambda: float, away_lambda: float):
    scores = []

    for home_goals in range(6):
        for away_goals in range(6):

            probability = (
                poisson(home_goals, home_lambda)
                * poisson(away_goals, away_lambda)
            )

            scores.append(
                (
                    f"{home_goals}-{away_goals}",
                    probability,
                )
            )

    scores.sort(
        key=lambda score: score[1],
        reverse=True,
    )

    return scores