from typing import List
from decimal import Decimal

from assetallocation_arp.data_etl.dal.strategy import Strategy
from assetallocation_arp.common_libraries.models_names import Models
from assetallocation_arp.common_libraries.leverage_types import Leverage
from assetallocation_arp.common_libraries.frequency_types import Frequency
from assetallocation_arp.common_libraries.day_of_week import DayOfWeek
from assetallocation_arp.data_etl.dal.validate import validate_enum


class Times(Strategy):
    def __init__(self, day_of_week: DayOfWeek, frequency: Frequency, leverage_type: Leverage, long_signals: List[Decimal],
                 short_signals: List[Decimal], time_lag_in_months: int, volatility_window: int):
        name = Models.times.name
        super().__init__(name)
        self._day_of_week = day_of_week
        self.frequency = frequency  # enum
        self.leverage_type = leverage_type
        self._long_signals = long_signals
        self._short_signals = short_signals
        self.time_lag = time_lag_in_months
        self._volatility_window = volatility_window

    @property
    def day_of_week(self):
        return self._day_of_week

    @day_of_week.setter
    def day_of_week(self, x):
        # TODO change below to not use Enum values
        validate_enum(x, DayOfWeek.__members__.values())
        self._day_of_week = x

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, x: Frequency):
        validate_enum(x, Frequency.__members__.keys())
        self._frequency = x

    @property
    def leverage_type(self):
        return self._leverage_type

    @leverage_type.setter
    def leverage_type(self, x: Leverage):
        validate_enum(x, Leverage.__members__.keys())
        self._leverage_type = x

    @property
    def long_signals(self):
        return self._long_signals

    @property
    def short_signals(self):
        return self._short_signals

    @property
    def time_lag(self):
        return self._time_lag

    @time_lag.setter
    def time_lag(self, x: int):
        self._time_lag = f'{-x} mons'

    @property
    def volatility_window(self):
        return self._volatility_window