from typing import List, Union
from decimal import Decimal
from abc import ABC

from assetallocation_arp.common_enums.strategy import TrendIndicator, CarryType, Frequency, DayOfWeek, Leverage, Name

from psycopg2.extras import DateTimeTZRange


class Strategy(ABC):
    def __init__(self, name: Union[str, Name]):
        self.name = name
        self._description = ''
        self._version = None

    @property
    def name(self) -> Name:
        return self._name

    @name.setter
    def name(self, x: Union[str, Name]) -> None:
        self._name = x if isinstance(x, Name) else Name[x]

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, x: str) -> None:
        self._description = x

    @property
    def version(self) -> int:
        return self._version

    @version.setter
    def version(self, x: int) -> None:
        self._version = x


class Times(Strategy):
    name = Name.times.name

    def __init__(self, day_of_week: Union[int, DayOfWeek], frequency: Union[str, Frequency],
                 leverage_type: Union[str, Leverage], long_signals: List[Decimal], short_signals: List[Decimal],
                 time_lag_in_months: int, volatility_window: int) -> None:
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
    def time_lag_interval(self) -> str:
        return self._time_lag_interval

    @time_lag_interval.setter
    def time_lag_interval(self, x: int) -> None:
        self._time_lag_interval = f'{-x} mons'

    @property
    def day_of_week(self) -> DayOfWeek:
        return self._day_of_week

    @day_of_week.setter
    def day_of_week(self, x: Union[int, DayOfWeek]) -> None:
        self._day_of_week = x if isinstance(x, DayOfWeek) else DayOfWeek(x)

    @property
    def frequency(self) -> Frequency:
        return self._frequency

    @frequency.setter
    def frequency(self, x: Union[str, Frequency]) -> None:
        self._frequency = x if isinstance(x, Frequency) else Frequency[x]

    @property
    def leverage_type(self) -> Leverage:
        return self._leverage_type

    @leverage_type.setter
    def leverage_type(self, x: Union[str, Leverage]) -> None:
        self._leverage_type = x if isinstance(x, Leverage) else Leverage[x]

    @property
    def long_signals(self) -> List[Decimal]:
        return self._long_signals

    @long_signals.setter
    def long_signals(self, x: List[Decimal]) -> None:
        self._long_signals = x
    
    @property
    def short_signals(self) -> List[Decimal]:
        return self._short_signals
    
    @short_signals.setter
    def short_signals(self, x: List[Decimal]) -> None:
        self._short_signals = x
    
    @property
    def time_lag_in_months(self) -> int:
        return self._time_lag_in_months

    @time_lag_in_months.setter
    def time_lag_in_months(self, x: int) -> None:
        self._time_lag_in_months = x

    @property
    def volatility_window(self) -> int:
        return self._volatility_window
    
    @volatility_window.setter
    def volatility_window(self, x: int) -> None:
        self._volatility_window = x
    

class Fica(Strategy):
    name = Name.fica.name

    def __init__(self, coupon: Decimal, curve: str, business_tstzrange: DateTimeTZRange,
                 strategy_weights: List[Decimal], tenor: int, trading_cost: int) -> None:
        super().__init__(self.name)
        self._coupon = coupon
        self._curve = curve
        self._business_tstzrange = business_tstzrange
        self._strategy_weights = strategy_weights
        self._tenor = tenor
        self._trading_cost = trading_cost

    @property
    def coupon(self) -> Decimal:
        return self._coupon
    
    @coupon.setter
    def coupon(self, x: Decimal) -> None:
        self._coupon = x
    
    @property
    def curve(self) -> str:
        return self._curve

    @curve.setter
    def curve(self, x: str) -> None:
        self._curve = x
    
    @property
    def business_tstzrange(self) -> DateTimeTZRange:
        return self._business_tstzrange

    @business_tstzrange.setter
    def business_tstzrange(self, x: DateTimeTZRange) -> None:
        self._business_tstzrange = x
    
    @property
    def strategy_weights(self) -> List[Decimal]:
        return self._strategy_weights
    
    @strategy_weights.setter
    def strategy_weights(self, x: List[Decimal]) -> None:
        self._strategy_weights = x
    
    @property
    def tenor(self) -> int:
        return self._tenor

    @tenor.setter
    def tenor(self, x: int) -> None:
        self._tenor = x
    
    @property
    def trading_cost(self) -> int:
        return self._trading_cost

    @trading_cost.setter
    def trading_cost(self, x: int) -> None:
        self._trading_cost = x


class Effect(Strategy):
    name = Name.effect.name

    def __init__(self, carry_type: str, closing_threshold: Decimal, cost: Decimal, day_of_week: Union[int, DayOfWeek],
                 frequency: Union[str, Frequency], include_shorts: bool, inflation_lag_in_months: int,
                 interest_rate_cut_off_long: Decimal, interest_rate_cut_off_short: Decimal,
                 moving_average_long_term: int, moving_average_short_term: int, is_realtime_inflation_forecast: bool,
                 trend_indicator: Union[str, TrendIndicator]) -> None:
        super().__init__(self.name)
        self.carry_type = carry_type
        self._closing_threshold = closing_threshold
        self._cost = cost
        self.day_of_week = day_of_week
        self.frequency = frequency
        self._include_shorts = include_shorts
        self.inflation_lag_in_months = inflation_lag_in_months
        self.inflation_lag_interval = inflation_lag_in_months
        self._interest_rate_cut_off_long = interest_rate_cut_off_long
        self._interest_rate_cut_off_short = interest_rate_cut_off_short
        self._moving_average_long_term = moving_average_long_term
        self._moving_average_short_term = moving_average_short_term
        self._is_realtime_inflation_forecast = is_realtime_inflation_forecast
        self.trend_indicator = trend_indicator

    @property
    def inflation_lag_interval(self) -> str:
        return self._inflation_lag_interval

    @inflation_lag_interval.setter
    def inflation_lag_interval(self, x: int) -> None:
        self._inflation_lag_interval =  f'{-x} mons'

    @property
    def carry_type(self) -> str:
        return self._carry_type

    @carry_type.setter
    def carry_type(self, x: Union[str, CarryType]) -> None:
        self._carry_type = x if isinstance(x, CarryType) else CarryType[x]

    @property
    def closing_threshold(self) -> Decimal:
        return self._closing_threshold

    @closing_threshold.setter
    def closing_threshold(self, x: Decimal) -> None:
        self._closing_threshold = x

    @property
    def cost(self) -> Decimal:
        return self._cost

    @cost.setter
    def cost(self, x: Decimal) -> None:
        self._cost = x

    @property
    def day_of_week(self) -> DayOfWeek:
        return self._day_of_week

    @day_of_week.setter
    def day_of_week(self, x: Union[int, DayOfWeek]) -> None:
        self._day_of_week = x if isinstance(x, DayOfWeek) else DayOfWeek(x)

    @property
    def frequency(self) -> Frequency:
        return self._frequency

    @frequency.setter
    def frequency(self, x: Union[str, Frequency]) -> None:
        self._frequency = x if isinstance(x, Frequency) else Frequency[x]

    @property
    def include_shorts(self) -> bool:
        return self._include_shorts

    @include_shorts.setter
    def include_shorts(self, x: bool) -> None:
        self._include_shorts = x

    @property
    def inflation_lag_in_months(self) -> str:
        return self._inflation_lag_in_months

    @inflation_lag_in_months.setter
    def inflation_lag_in_months(self, x: int):
        self._inflation_lag_in_months = x

    @property
    def interest_rate_cut_off_long(self) -> Decimal:
        return self._interest_rate_cut_off_long

    @interest_rate_cut_off_long.setter
    def interest_rate_cut_off_long(self, x: Decimal) -> None:
        self._interest_rate_cut_off_long = x

    @property
    def interest_rate_cut_off_short(self) -> Decimal:
        return self._interest_rate_cut_off_short

    @interest_rate_cut_off_short.setter
    def interest_rate_cut_off_short(self, x: Decimal) -> None:
        self._interest_rate_cut_off_short = x

    @property
    def moving_average_long_term(self) -> int:
        return self._moving_average_long_term

    @moving_average_long_term.setter
    def moving_average_long_term(self, x: int) -> None:
        self._moving_average_long_term = x

    @property
    def moving_average_short_term(self) -> int:
        return self._moving_average_short_term

    @moving_average_short_term.setter
    def moving_average_short_term(self, x: int) -> None:
        self._moving_average_short_term = x

    @property
    def is_realtime_inflation_forecast(self) -> bool:
        return self._is_realtime_inflation_forecast

    @is_realtime_inflation_forecast.setter
    def is_realtime_inflation_forecast(self, x: bool) -> None:
        self._is_realtime_inflation_forecast = x

    @property
    def trend_indicator(self) -> TrendIndicator:
        return self._trend_indicator

    @trend_indicator.setter
    def trend_indicator(self, x: Union[str, TrendIndicator]) -> None:
        self._trend_indicator = x if isinstance(x, TrendIndicator) else TrendIndicator[x]
