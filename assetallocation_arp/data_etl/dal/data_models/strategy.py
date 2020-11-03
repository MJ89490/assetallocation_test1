from typing import List, Union, Optional, Tuple
from abc import ABC, abstractmethod

from psycopg2.extras import DateTimeTZRange

from assetallocation_arp.common_libraries.dal_enums.strategy import TrendIndicator, CarryType, Frequency, DayOfWeek, \
    Leverage, Name, FxModel
from assetallocation_arp.data_etl.dal.type_converter import ArpTypeConverter
from assetallocation_arp.data_etl.dal.data_models.asset import EffectAssetInput, TimesAssetInput, FicaAssetInput, \
    FxAssetInput, Asset
from assetallocation_arp.data_etl.dal.data_models.fund_strategy import FundStrategyAnalytic, FundStrategyAssetWeight
from assetallocation_arp.data_etl.dal.data_frame_converter import TimesDataFrameConverter, FicaDataFrameConverter
from assetallocation_arp.common_libraries.dal_enums.fica_asset_input import Category
from assetallocation_arp.models import times, fica


# noinspection PyAttributeOutsideInit
class Strategy(ABC):
    def __init__(self, name: Union[str, Name]):
        """Strategy class to hold data from database"""
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

    @abstractmethod
    def run(self) -> Tuple[List[FundStrategyAnalytic], List[FundStrategyAssetWeight]]:
        pass


# noinspection PyAttributeOutsideInit
class Times(Strategy):
    name = Name.times.name

    def __init__(self, day_of_week: Union[int, DayOfWeek], frequency: Union[str, Frequency],
                 leverage_type: Union[str, Leverage], long_signals: List[float], short_signals: List[float],
                 time_lag_in_months: int, volatility_window: int) -> None:
        """Times class to hold data from database"""
        super().__init__(self.name)
        self.day_of_week = day_of_week
        self.frequency = frequency
        self.leverage_type = leverage_type
        self._long_signals = long_signals
        self._short_signals = short_signals
        self.time_lag_in_months = time_lag_in_months
        self._volatility_window = volatility_window
        self._asset_inputs = []

    @property
    def asset_inputs(self) -> List[TimesAssetInput]:
        return self._asset_inputs

    @asset_inputs.setter
    def asset_inputs(self, x: List[TimesAssetInput]) -> None:
        self._asset_inputs = x

    @property
    def time_lag_interval(self) -> str:
        return ArpTypeConverter.month_lag_int_to_interval(self.time_lag_in_months)

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
    def long_signals(self) -> List[float]:
        return self._long_signals

    @long_signals.setter
    def long_signals(self, x: List[float]) -> None:
        self._long_signals = x
    
    @property
    def short_signals(self) -> List[float]:
        return self._short_signals
    
    @short_signals.setter
    def short_signals(self, x: List[float]) -> None:
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

    def run(self) -> Tuple[List[FundStrategyAnalytic], List[FundStrategyAssetWeight]]:
        signals, returns, r, positioning = times.calculate_signals_returns_r_positioning(self)
        asset_analytics = TimesDataFrameConverter.create_asset_analytics(signals, returns, r, self.frequency)
        asset_weights = TimesDataFrameConverter.df_to_asset_weights(positioning, Frequency.daily)
        return asset_analytics, asset_weights
    

class Fica(Strategy):
    name = Name.fica.name

    def __init__(self, coupon: float, curve: str, business_tstzrange: DateTimeTZRange,
                 strategy_weights: List[float], tenor: int, trading_cost: int) -> None:
        """Fica class to hold data from database"""
        super().__init__(self.name)
        self._coupon = coupon
        self._curve = curve
        self._business_tstzrange = business_tstzrange
        self._strategy_weights = strategy_weights
        self._tenor = tenor
        self._trading_cost = trading_cost
        self._grouped_asset_inputs = []

    @property
    def grouped_asset_inputs(self) -> List[List[FicaAssetInput]]:
        return self._grouped_asset_inputs

    @grouped_asset_inputs.setter
    def grouped_asset_inputs(self, x: List[List[FicaAssetInput]]) -> None:
        self._grouped_asset_inputs = x

    @property
    def coupon(self) -> float:
        return self._coupon
    
    @coupon.setter
    def coupon(self, x: float) -> None:
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
    def strategy_weights(self) -> List[float]:
        return self._strategy_weights
    
    @strategy_weights.setter
    def strategy_weights(self, x: List[float]) -> None:
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

    def run(self) -> Tuple[List[FundStrategyAnalytic], List[FundStrategyAssetWeight]]:
        curve = fica.format_data(self)
        carry_roll, country_returns = fica.calculate_carry_roll_down(self, curve)
        signals, cum_contribution, returns = fica.calculate_signals_and_returns(self, carry_roll, country_returns)
        carry_daily, return_daily = fica.run_daily_attribution(self, signals)

        carry_total_cols = ['fica_10y_carry', 'fica_10y_carry_cum', 'G3_10y_carry']
        return_total_cols = ['fica_10y_spot', 'fica_10y_spot_cum', 'fica_10y_return', 'fica_10y_return%',
                             'correlation', 'beta', 'G3_10y_return', 'G3_10y_return%']
        contribution_total_col = 'Return'
        strategy_analytics = FicaDataFrameConverter.create_strategy_analytics(
            cum_contribution[contribution_total_col], returns, carry_roll['fica_10y_carry'],
            carry_daily['fica_10y_return', 'fica_10y_return%', 'correlation', 'beta']
        )
        comparator_analytics = FicaDataFrameConverter.create_comparator_analytics(
            carry_roll['G3_10y_carry'], carry_daily['G3_10y_return', 'G3_10y_return%'])

        future_tickers = [
            asset.ticker for group in self.grouped_asset_inputs for asset in group if
            asset.input_category == Category.future
        ]
        asset_analytics = FicaDataFrameConverter.create_asset_analytics(
            carry_roll.drop(carry_total_cols), cum_contribution.drop(contribution_total_col),
            carry_daily.drop(return_total_cols), return_daily, future_tickers
        )
        analytics = strategy_analytics + comparator_analytics + asset_analytics

        asset_weights = FicaDataFrameConverter.df_to_asset_weights(signals, Frequency.monthly)
        return analytics, asset_weights


# noinspection PyAttributeOutsideInit
class Effect(Strategy):
    name = Name.effect.name

    def __init__(self, carry_type: Union[str, CarryType], closing_threshold: float, cost: float,
                 day_of_week: Union[int, DayOfWeek], frequency: Union[str, Frequency], include_shorts: bool,
                 inflation_lag_in_months: int, interest_rate_cut_off_long: float, interest_rate_cut_off_short: float,
                 moving_average_long_term: int, moving_average_short_term: int, is_realtime_inflation_forecast: bool,
                 trend_indicator: Union[str, TrendIndicator]) -> None:
        """Effect class to hold data from database"""
        super().__init__(self.name)
        self.carry_type = carry_type
        self.closing_threshold = closing_threshold
        self.cost = cost
        self.day_of_week = day_of_week
        self.frequency = frequency
        self.include_shorts = include_shorts
        self.inflation_lag_in_months = inflation_lag_in_months
        self.interest_rate_cut_off_long = interest_rate_cut_off_long
        self.interest_rate_cut_off_short = interest_rate_cut_off_short
        self.moving_average_long_term = moving_average_long_term
        self.moving_average_short_term = moving_average_short_term
        self.is_realtime_inflation_forecast = is_realtime_inflation_forecast
        self.trend_indicator = trend_indicator
        self._asset_inputs = []

    @property
    def asset_inputs(self) -> List[EffectAssetInput]:
        return self._asset_inputs

    @asset_inputs.setter
    def asset_inputs(self, x: List[EffectAssetInput]) -> None:
        self._asset_inputs = x

    @property
    def inflation_lag_interval(self) -> str:
        return ArpTypeConverter.month_lag_int_to_interval(self.inflation_lag_in_months)

    @property
    def carry_type(self) -> CarryType:
        return self._carry_type

    @carry_type.setter
    def carry_type(self, x: Union[str, CarryType]) -> None:
        self._carry_type = x if isinstance(x, CarryType) else CarryType[x]

    @property
    def closing_threshold(self) -> float:
        return self._closing_threshold

    @closing_threshold.setter
    def closing_threshold(self, x: float) -> None:
        self._closing_threshold = x

    @property
    def cost(self) -> float:
        return self._cost

    @cost.setter
    def cost(self, x: float) -> None:
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
    def inflation_lag_in_months(self) -> int:
        return self._inflation_lag_in_months

    @inflation_lag_in_months.setter
    def inflation_lag_in_months(self, x: int):
        self._inflation_lag_in_months = x

    @property
    def interest_rate_cut_off_long(self) -> float:
        return self._interest_rate_cut_off_long

    @interest_rate_cut_off_long.setter
    def interest_rate_cut_off_long(self, x: float) -> None:
        self._interest_rate_cut_off_long = x

    @property
    def interest_rate_cut_off_short(self) -> float:
        return self._interest_rate_cut_off_short

    @interest_rate_cut_off_short.setter
    def interest_rate_cut_off_short(self, x: float) -> None:
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

    def run(self) -> Tuple[List[FundStrategyAnalytic], List[FundStrategyAssetWeight]]:
        """Run effect strategy and return FundStrategyAssetAnalytics and FundStrategyAssetWeights"""
        # TODO add code to run effect, using Effect object, here
        pass


# noinspection PyAttributeOutsideInit
class Fx(Strategy):
    name = Name.fx.name

    def __init__(
            self, model: str, business_tstzrange: DateTimeTZRange, signal: str, currency: str, response_function: bool,
            exposure: float, momentum_weights: List[float], transaction_cost: float
    ) -> None:
        super().__init__(self.name)
        self.model = model
        self.business_tstzrange = business_tstzrange
        self.signal = signal
        self.currency = currency
        self.response_function = response_function
        self.exposure = exposure
        self.momentum_weights = momentum_weights
        self.transaction_cost = transaction_cost
        self.top_crosses = None
        self.vol_window = None
        self.value_window = None
        self.sharpe_cutoff = None
        self.mean_reversion = None
        self.historical_base = None
        self.asset_inputs = []
        self.carry_assets = []
        self.spot_assets = []

    @property
    def spot_assets(self) -> List[Asset]:
        return self._spot_asset

    @spot_assets.setter
    def spot_assets(self, x: List[Asset]) -> None:
        self._spot_asset = x

    @property
    def carry_assets(self) -> List[Asset]:
        return self._carry_asset

    @carry_assets.setter
    def carry_assets(self, x: List[Asset]) -> None:
        self._carry_asset = x

    @property
    def model(self) -> Union[str, FxModel]:
        return self._model

    @model.setter
    def model(self, x: Union[str, FxModel]) -> None:
        self._model = x if isinstance(x, FxModel) else FxModel[x]

    @property
    def asset_inputs(self) -> List[FxAssetInput]:
        return self._asset_inputs

    @asset_inputs.setter
    def asset_inputs(self, x: List[FxAssetInput]) -> None:
        self._asset_inputs = x

    @property
    def top_crosses(self) -> Optional[int]:
        return self._top_crosses

    @top_crosses.setter
    def top_crosses(self, x: Optional[int]) -> None:
        self._top_crosses = x

    @property
    def historical_base(self) -> Optional[int]:
        return self._historical_base

    @historical_base.setter
    def historical_base(self, x: Optional[int]) -> None:
        self._historical_base = x

    @property
    def mean_reversion(self) -> Optional[int]:
        return self._mean_reversion

    @mean_reversion.setter
    def mean_reversion(self, x: Optional[int]) -> None:
        self._mean_reversion = x

    @property
    def sharpe_cutoff(self) -> Optional[int]:
        return self._sharpe_cutoff

    @sharpe_cutoff.setter
    def sharpe_cutoff(self, x: Optional[int]) -> None:
        self._sharpe_cutoff = x

    @property
    def vol_window(self) -> Optional[int]:
        return self._vol_window

    @vol_window.setter
    def vol_window(self, x: Optional[int]) -> None:
        self._vol_window = x

    def run(self) -> Tuple[List[FundStrategyAnalytic], List[FundStrategyAssetWeight]]:
        # spot, carry, cash, ppp = fxmodels.format_data(strategy)
        # signal, volatility = fxmodels.calculate_signals(strategy, spot, carry, cash, ppp)
        # fx_model, exposure, exposure_agg = fxmodels.determine_sizing(strategy, signal, volatility)
        # base_fx, returns, contribution, carry_base = fxmodels.calculate_returns(strategy, carry, signal, exposure,
        #                                                                         exposure_agg)
        #
        # asset_analytics = FxDataFrameConverter.create_asset_analytics(signals, returns, r, strategy.frequency)
        # asset_weights = FxDataFrameConverter.df_to_asset_weights(positioning, Frequency.daily)
        # return asset_analytics, asset_weights
        pass
