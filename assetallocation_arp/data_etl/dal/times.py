from typing import List

from psycopg2.extras import DateTimeTZRange

from .strategy import Strategy
from .user import User


class Times(Strategy):
    def __init__(self, description: str, strategy_id: int, name: str, system_tstzrange: DateTimeTZRange, user: User,
                 day_of_week: int, frequency: str, leverage_type: str, long_signals: List[float],
                 short_signals: List[float], strategy: Strategy, time_lag: int, volatility_window: int):
        super().__init__(description, strategy_id, name, system_tstzrange, user)
        self._day_of_week = day_of_week
        self._frequency = frequency  # enum
        self._leverage_type = leverage_type
        self._long_signals = long_signals
        self._short_signals = short_signals
        self._strategy = strategy
        self._time_lag = time_lag
        self._volatility_window = volatility_window
