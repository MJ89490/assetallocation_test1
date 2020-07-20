from typing import List, Optional

from .strategy import Strategy
from .user import User
from .db import Db

from assetallocation_arp.common_libraries.models_names import Models


class Times(Strategy):
    def __init__(self, user: User, day_of_week: int, frequency: str, leverage_type: str, long_signals: List[float],
                 short_signals: List[float], time_lag: int, volatility_window: int, description: Optional[str] = None):
        name = Models.times.name
        super().__init__(name, user, description)
        self._day_of_week = day_of_week
        self._frequency = frequency  # enum
        self._leverage_type = leverage_type
        self._long_signals = long_signals
        self._short_signals = short_signals
        self._time_lag = time_lag
        self._volatility_window = volatility_window

    @property
    def day_of_week(self):
        return self._day_of_week

    @property
    def frequency(self):
        return self._frequency

    @property
    def leverage_type(self):
        return self._leverage_type

    @property
    def long_signals(self):
        return self._long_signals

    @property
    def short_signals(self):
        return self._short_signals

    @property
    def time_lag(self):
        return self._time_lag

    @property
    def volatility_window(self):
        return self._volatility_window

    def insert(self, db: Db, asset_tickers: List[str]) -> int:
        strategy_id = db.call_proc('insert_times_strategy',
                                   [self.name, self.description, self.user.user_id, self.day_of_week, self.frequency,
                                    self.leverage_type, self.long_signals, self.short_signals, self.time_lag,
                                    self.volatility_window, asset_tickers])

        return strategy_id[0]

    def get_id(self, db: Db) -> Optional[int]:
        strategy_id = db.get_times_strategy_id(self.name, self.description, self.day_of_week,
                                               self.frequency, self.leverage_type, self.long_signals,
                                               self.short_signals, self.time_lag, self.volatility_window)

        return strategy_id
