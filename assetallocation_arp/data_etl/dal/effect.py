from psycopg2.extras import DateTimeTZRange

from .strategy import Strategy
from .user import User


class Effect(Strategy):
    def __init__(self, description: str, strategy_id: int, name: str, system_tstzrange: DateTimeTZRange, user: User,
                 carry_type: str, closing_threshold: float, cost: float, day_of_week: int, frequency: str,
                 include_shorts_flag: bool, inflation_lag: int, interest_rate_cut_off_long: float,
                 interest_rate_cut_off_short: float, moving_average_long_term: int, moving_average_short_term: int,
                 realtime_inflation_forecast_flag: bool, strategy: Strategy, trend_indicator: str):
        super().__init__(description, strategy_id, name, system_tstzrange, user)
        self._carry_type = carry_type  # 'Nominal' or 'Real'
        self._closing_threshold = closing_threshold
        self._cost = cost
        self._day_of_week = day_of_week
        self._frequency = frequency
        self._include_shorts_flag = include_shorts_flag
        self._inflation_lag = inflation_lag
        self._interest_rate_cut_off_long = interest_rate_cut_off_long
        self._interest_rate_cut_off_short = interest_rate_cut_off_short
        self._moving_average_long_term = moving_average_long_term
        self._moving_average_short_term = moving_average_short_term
        self._realtime_inflation_forecast_flag = realtime_inflation_forecast_flag
        self._strategy = strategy
        self._trend_indicator = trend_indicator  # 'TotalReturn', 'Spot'

