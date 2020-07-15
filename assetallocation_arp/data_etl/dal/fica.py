from typing import List

from psycopg2.extras import DateTimeTZRange

from .strategy import Strategy
from .user import User


class Fica(Strategy):
    def __init__(self, description: str, strategy_id: int, name: str, system_tstzrange: DateTimeTZRange, user: User,
                 coupon: float, curve: str, date_from: str, date_to: str, strategy: Strategy,
                 strategy_weights: List[float], tenor: int, trading_cost: int):
        super().__init__(description, strategy_id, name, system_tstzrange, user)
        self._coupon = coupon
        self._curve = curve
        self._date_from = date_from
        self._date_to = date_to
        self._strategy = strategy
        self._strategy_weights = strategy_weights
        self._tenor = tenor
        self._trading_cost = trading_cost
