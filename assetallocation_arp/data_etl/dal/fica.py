from typing import List

from psycopg2.extras import DateTimeTZRange

from .strategy import Strategy
from .user import User
from .db import Db


class Fica(Strategy):
    def __init__(self, description: str, name: str, user: User, coupon: float, curve: str,
                 business_tstzrange: DateTimeTZRange, strategy_weights: List[float], tenor: int, trading_cost: int):
        super().__init__(name, user, description)
        self._coupon = coupon
        self._curve = curve
        self._business_tstzrange = business_tstzrange
        self._strategy_weights = strategy_weights
        self._tenor = tenor
        self._trading_cost = trading_cost

    @property
    def coupon(self):
        return self._coupon

    @property
    def curve(self):
        return self._curve

    @property
    def business_tstzrange(self):
        return self._business_tstzrange

    @property
    def strategy_weights(self):
        return self._strategy_weights

    @property
    def tenor(self):
        return self._tenor

    @property
    def trading_cost(self):
        return self._trading_cost

    def insert(self, db: Db):
        self._version = db.call_proc('insert_fica_strategy',
                                              [self.name, self.description, self.user.user_id, self.coupon, self.curve,
                                               self.business_tstzrange, str(self.strategy_weights), self.tenor,
                                               self.trading_cost])
