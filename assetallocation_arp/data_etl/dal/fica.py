from typing import List

from .strategy import Strategy


class Fica:
    def __init__(self, coupon: float, curve: str, date_from: str, date_to: str, strategy: Strategy,
                 strategy_weights: List[float], tenor: int, trading_cost: int):
        self._coupon = coupon
        self._curve = curve
        self._date_from = date_from
        self._date_to = date_to
        self._strategy = strategy
        self._strategy_weights = strategy_weights
        self._tenor = tenor
        self._trading_cost = trading_cost
