from decimal import Decimal

from datetime import datetime


class FundStrategy:
    def __init__(self, business_datetime: datetime, save_output_flag: bool,
                 weight: Decimal):
        self._business_datetime = business_datetime
        self._fund_strategy_id = None
        self._save_output_flag = save_output_flag
        self._system_datetime = None
        self._weight = weight

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
