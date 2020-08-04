from typing import List
from decimal import Decimal
from abc import ABC

from assetallocation_arp.data_etl.dal.validate import check_value
from assetallocation_arp.common_enums.strategy import TrendIndicator, CarryType, Frequency, DayOfWeek, Leverage, Name

from psycopg2.extras import DateTimeTZRange


class Strategy(ABC):
    def __init__(self, name: str):
        self.name = name
        self._description = ''
        self._version = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, x):
        check_value(x, Name.__members__.keys())
        self._name = x

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, x: str):
        self._description = x

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, x: int):
        self._version = x


class Times(Strategy):
    name = Name.times.name

    def __init__(self, day_of_week: DayOfWeek, frequency: Frequency, leverage_type: Leverage,
                 long_signals: List[Decimal], short_signals: List[Decimal], time_lag_in_months: int,
                 volatility_window: int):
        super().__init__(self.name)
        self._day_of_week = day_of_week
        self.frequency = frequency
        self.leverage_type = leverage_type
        self._long_signals = long_signals
        self._short_signals = short_signals
        self.time_lag_in_months = time_lag_in_months
        self.time_lag_interval = time_lag_in_months
        self._volatility_window = volatility_window

    @property
    def time_lag_interval(self):
        return self._time_lag_interval

    @time_lag_interval.setter
    def time_lag_interval(self, x: int):
        self._time_lag_interval = f'{-x} mons'

    @property
    def day_of_week(self):
        return self._day_of_week

    @day_of_week.setter
    def day_of_week(self, x):
        # TODO change below to not use Enum values
        check_value(x, DayOfWeek.__members__.values())
        self._day_of_week = x

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, x: Frequency):
        check_value(x, Frequency.__members__.keys())
        self._frequency = x

    @property
    def leverage_type(self):
        return self._leverage_type

    @leverage_type.setter
    def leverage_type(self, x: Leverage):
        check_value(x, Leverage.__members__.keys())
        self._leverage_type = x

    @property
    def long_signals(self):
        return self._long_signals

    @property
    def short_signals(self):
        return self._short_signals

    @property
    def time_lag_in_months(self):
        return self._time_lag_in_months

    @time_lag_in_months.setter
    def time_lag_in_months(self, x: int):
        self._time_lag_in_months = x

    @property
    def volatility_window(self):
        return self._volatility_window


class Fica(Strategy):
    name = Name.fica.name

    def __init__(self, name: str, coupon: float, curve: str, business_tstzrange: DateTimeTZRange,
                 strategy_weights: List[float], tenor: int, trading_cost: int):
        super().__init__(name)
        self._coupon = coupon
        self._curve = curve
        self._business_tstzrange = business_tstzrange
        self._strategy_weights = strategy_weights
        self._tenor = tenor
        self._trading_cost = trading_cost

    @property
    def coupon(self):
        return self._coupon

    @property
    def curve(self):
        return self._curve

    @property
    def business_tstzrange(self):
        return self._business_tstzrange

    @property
    def strategy_weights(self):
        return self._strategy_weights

    @property
    def tenor(self):
        return self._tenor

    @property
    def trading_cost(self):
        return self._trading_cost


class Effect(Strategy):
    name = Name.effect.name

    def __init__(self, carry_type: str, closing_threshold: Decimal, cost: Decimal, day_of_week: DayOfWeek,
                 frequency: Frequency, include_shorts: bool, inflation_lag_in_months: int,
                 interest_rate_cut_off_long: Decimal, interest_rate_cut_off_short: Decimal,
                 moving_average_long_term: int, moving_average_short_term: int, is_realtime_inflation_forecast: bool,
                 trend_indicator: TrendIndicator):
        super().__init__(self.name)
        self.carry_type = carry_type
        self._closing_threshold = closing_threshold
        self._cost = cost
        self.day_of_week = day_of_week
        self.frequency = frequency
        self._include_shorts = include_shorts
        self._inflation_lag = inflation_lag_in_months
        self._interest_rate_cut_off_long = interest_rate_cut_off_long
        self._interest_rate_cut_off_short = interest_rate_cut_off_short
        self._moving_average_long_term = moving_average_long_term
        self._moving_average_short_term = moving_average_short_term
        self._is_realtime_inflation_forecast = is_realtime_inflation_forecast
        self.trend_indicator = trend_indicator

    @property
    def carry_type(self):
        return self._carry_type

    @carry_type.setter
    def carry_type(self, x: CarryType):
        check_value(x, CarryType.__members__.keys())
        self._carry_type = x

    @property
    def closing_threshold(self):
        return self._closing_threshold

    @property
    def cost(self):
        return self._cost

    @property
    def day_of_week(self):
        return self._day_of_week

    @day_of_week.setter
    def day_of_week(self, x):
        # TODO change below to not use Enum values
        check_value(x, DayOfWeek.__members__.values())
        self._day_of_week = x

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, x: Frequency):
        check_value(x, Frequency.__members__.keys())
        self._frequency = x

    @property
    def include_shorts(self):
        return self._include_shorts

    @property
    def inflation_lag(self):
        return self._inflation_lag

    @inflation_lag.setter
    def inflation_lag(self, x: int):
        self._inflation_lag = f'{-x} mons'

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
    def is_realtime_inflation_forecast(self):
        return self._is_realtime_inflation_forecast

    @property
    def trend_indicator(self):
        return self._trend_indicator

    @trend_indicator.setter
    def trend_indicator(self, x: TrendIndicator):
        check_value(x, TrendIndicator.__members__.keys())
        self._trend_indicator = x
