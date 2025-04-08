from math import prod

def moneyline_to_decimal(ml: float) -> float:
    """
    Convert American (moneyline) odds to decimal odds.
    For positive moneyline: decimal = 1 + (ml / 100)
    For negative moneyline: decimal = 1 + (100 / |ml|)
    """
    if ml > 0:
        return 1 + (ml / 100.0)
    else:
        return 1 + (100.0 / abs(ml))

def decimal_to_moneyline(dec: float) -> float:
    """
    Convert decimal odds to American moneyline odds.
    """
    if dec >= 2.0:
        return (dec - 1.0) * 100.0
    else:
        return -100.0 / (dec - 1.0)

def calculate_parlay_probability(fair_probs: list[float]) -> float:
    """
    Multiply the fair (true) probabilities of each leg
    to get the overall fair probability of the parlay.
    """
    return prod(fair_probs)

def calculate_ev_of_parlay(fair_parlay_prob: float, offered_parlay_moneyline: float, stake: float = 1.0) -> float:
    """
    Calculate the expected value (EV) of a parlay bet.
    EV = p_win * (offered_decimal_odds * stake) - stake,
    where p_win is the overall fair (model) parlay probability.
    """
    dec_odds = moneyline_to_decimal(offered_parlay_moneyline)
    return fair_parlay_prob * dec_odds * stake - stake

def kelly_fraction(dec_odds: float, p: float) -> float:
    """
    Calculate the full Kelly fraction for a bet.
    Kelly fraction f = (dec_odds * p - 1) / (dec_odds - 1),
    provided the odds are > 1; otherwise, returns 0.
    """
    if dec_odds > 1:
        return max((dec_odds * p - 1) / (dec_odds - 1), 0)
    return 0.0

def american_to_probability(ml):
    """
    Convert American odds to implied probability.
    For positive odds: probability = 100 / (odds + 100)
    For negative odds: probability = -odds / (-odds + 100)
    """
    if ml > 0:
        return 100 / (ml + 100)
    elif ml < 0:
        return -ml / (-ml + 100)
    else:
        return 0  # odds value of 0 isn't valid for these calculations