from datetime import datetime

from .user import User
from .fund import Fund
from .strategy import Strategy
from .db import Db


class FundStrategy:
    def __init__(self, business_datetime: datetime, fund: Fund, save_output_flag: bool, strategy: Strategy,
                 weight: float, user: User):
        self._business_datetime = business_datetime
        self._fund = fund
        self._fund_strategy_id = None
        self._save_output_flag = save_output_flag
        self._strategy = strategy
        self._system_datetime = None
        self._weight = weight
        self._user = user

    @property
    def business_datetime(self):
        return self._business_datetime

    @property
    def fund(self):
        return self._fund

    @property
    def fund_strategy_id(self):
        return self._fund_strategy_id

    @property
    def save_output_flag(self):
        return self._save_output_flag

    @property
    def strategy(self):
        return self._strategy

    @property
    def system_datetime(self):
        return self._system_datetime

    @property
    def weight(self):
        return self._weight

    @property
    def user(self):
        return self._user

    def insert(self, db: Db):
        self._fund_strategy_id, self._system_datetime = db.call_proc('insert_fund_strategy',
                                                                     [self.business_datetime, self.fund.fund_id,
                                                                      self.save_output_flag, self.strategy, self.weight,
                                                                      self.user.user_id])
