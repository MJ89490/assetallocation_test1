from typing import List, Optional
from decimal import Decimal

from assetallocation_arp.data_etl.dal.strategy import Strategy

from assetallocation_arp.common_libraries.models_names import Models


class Times(Strategy):
    def __init__(self, day_of_week: int, frequency: str, leverage_type: str, long_signals: List[Decimal],
                 short_signals: List[Decimal], time_lag: int, volatility_window: int, description: Optional[str] = None):
        name = Models.times.name
        super().__init__(name, description)
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
        return f'{-self._time_lag} mons'

    @property
    def volatility_window(self):
        return self._volatility_window
