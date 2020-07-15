from datetime import datetime

from .user import User
from .fund import Fund
from .strategy import Strategy


class FundStrategy:
    def __init__(self, business_datetime: datetime, fund: Fund, fund_strategy_id: int, save_output_flag: bool,
                 strategy: Strategy, system_datetime: datetime, weight: float, user: User):
        self._business_datetime = business_datetime
        self._fund = fund
        self._id = fund_strategy_id
        self._save_output_flag = save_output_flag
        self._strategy_id = strategy
        self._system_datetime = system_datetime
        self._weight = weight
        self._user = user
