from typing import List

from .strategy import Strategy


class Times:
    def __init__(self, day_of_week: int, frequency: str, leverage_type: str, long_signals: List[float],
                 short_signals: List[float], strategy: Strategy, time_lag: int, volatility_window: int):
        self._day_of_week = day_of_week
        self._frequency = frequency  # enum
        self._leverage_type = leverage_type
        self._long_signals = long_signals
        self._short_signals = short_signals
        self._strategy = strategy
        self._time_lag = time_lag
        self._volatility_window = volatility_window
