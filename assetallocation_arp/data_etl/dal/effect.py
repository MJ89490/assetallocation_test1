from typing import Optional

from .strategy import Strategy
from .user import User
from.db import Db


class Effect(Strategy):
    def __init__(self, name: str, user: User,
                 carry_type: str, closing_threshold: float, cost: float, day_of_week: int, frequency: str,
                 include_shorts_flag: bool, inflation_lag: int, interest_rate_cut_off_long: float,
                 interest_rate_cut_off_short: float, moving_average_long_term: int, moving_average_short_term: int,
                 realtime_inflation_forecast_flag: bool, trend_indicator: str, description: Optional[str] = None):
        super().__init__(name, user, description)
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
        self._trend_indicator = trend_indicator  # 'TotalReturn', 'Spot'

    @property
    def carry_type(self):
        return self._carry_type

    @property
    def closing_threshold(self):
        return self._closing_threshold

    @property
    def cost(self):
        return self._cost

    @property
    def day_of_week(self):
        return self._day_of_week

    @property
    def frequency(self):
        return self._frequency

    @property
    def include_shorts_flag(self):
        return self._include_shorts_flag

    @property
    def inflation_lag(self):
        return self._inflation_lag

    @property
    def interest_rate_cut_off_long(self):
        return self._interest_rate_cut_off_long

    @property
    def interest_rate_cut_off_short(self):
        return self._interest_rate_cut_off_short

    @property
    def moving_average_long_term(self):
        return self._moving_average_long_term

    @property
    def moving_average_short_term(self):
        return self._moving_average_short_term

    @property
    def realtime_inflation_forecast_flag(self):
        return self._realtime_inflation_forecast_flag

    @property
    def trend_indicator(self):
        return self._trend_indicator

    def insert(self, db: Db):
        self._strategy_id, self._system_tstzrange = db.call_proc('add_effect_strategy',
                                                                 [self.name, self.description, self.user.user_id,
                                                                  self.carry_type, self.closing_threshold, self.cost,
                                                                  self.day_of_week, self.frequency,
                                                                  self.include_shorts_flag, self.inflation_lag,
                                                                  self.interest_rate_cut_off_long,
                                                                  self.interest_rate_cut_off_short,
                                                                  self.moving_average_long_term,
                                                                  self.moving_average_short_term,
                                                                  self.realtime_inflation_forecast_flag,
                                                                  self.trend_indicator])
