from typing import List, Union, Optional, Tuple
from abc import ABC, abstractmethod

from psycopg2.extras import DateTimeTZRange

from assetallocation_arp.common_libraries.dal_enums.strategy import TrendIndicator, CarryType, Frequency, DayOfWeek, \
    Leverage, Name, FxModel
from assetallocation_arp.common_libraries.dal_enums.fica_asset_input import CurveName
from assetallocation_arp.data_etl.dal.type_converter import ArpTypeConverter
from assetallocation_arp.data_etl.dal.data_models.asset import EffectAssetInput, TimesAssetInput, \
    FxAssetInput, Asset, FicaAssetInputGroup, MavenAssetInput
from assetallocation_arp.data_etl.dal.data_models.fund_strategy import FundStrategyAnalytic, FundStrategyAssetWeight
from assetallocation_arp.data_etl.dal.data_frame_converter import TimesDataFrameConverter, FicaDataFrameConverter, \
    FxDataFrameConverter, MavenDataFrameConverter
from assetallocation_arp.models import times, fica, fxmodels, maven


# noinspection PyAttributeOutsideInit
class Strategy(ABC):
    def __init__(self, name: Union[str, Name]):
        """Strategy class to hold data from database"""
        self.name = name
        self.description = ''
        self.version = None

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
    def version(self) -> Optional[int]:
        return self._version

    @version.setter
    def version(self, x: Optional[int]) -> None:
        self._version = x

    @abstractmethod
    def run(self) -> Tuple[List[FundStrategyAnalytic], List[FundStrategyAssetWeight]]:
        """Run strategy to produce outputs of FundStrategyAnalytics and FundStrategyAssetWeights"""
        pass


# noinspection PyAttributeOutsideInit
class Times(Strategy):
    def __init__(self, day_of_week: Union[int, DayOfWeek], frequency: Union[str, Frequency],
                 leverage_type: Union[str, Leverage], long_signals: List[float], short_signals: List[float],
                 time_lag_in_months: int, volatility_window: int) -> None:
        """Times class to hold data from database"""
        super().__init__(Name.times)
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
        ticker_map = {i.asset_subcategory: i.future_ticker for i in self.asset_inputs}
        asset_weights = TimesDataFrameConverter.df_to_asset_weights(positioning, Frequency.daily, ticker_map)
        return asset_analytics, asset_weights
    

class Fica(Strategy):
    def __init__(self, coupon: float, curve: Union[str, CurveName], strategy_weights: List[float], tenor: int, trading_cost: int) -> None:
        """Fica class to hold data from database"""
        super().__init__(Name.fica)
        self._coupon = coupon
        self._curve = curve
        self._strategy_weights = strategy_weights
        self._tenor = tenor
        self._trading_cost = trading_cost
        self._grouped_asset_inputs = []

    @property
    def grouped_asset_inputs(self) -> List[FicaAssetInputGroup]:
        return self._grouped_asset_inputs

    @grouped_asset_inputs.setter
    def grouped_asset_inputs(self, x: List[FicaAssetInputGroup]) -> None:
        self._grouped_asset_inputs = x

    @property
    def coupon(self) -> float:
        return self._coupon
    
    @coupon.setter
    def coupon(self, x: float) -> None:
        self._coupon = x
    
    @property
    def curve(self) -> CurveName:
        return self._curve

    @curve.setter
    def curve(self, x: str) -> None:
        self._curve = x if isinstance(x, CurveName) else CurveName[x]
    
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

        asset_analytics = FicaDataFrameConverter.create_asset_analytics(
            carry_roll.drop(carry_total_cols), cum_contribution.drop(contribution_total_col),
            carry_daily.drop(return_total_cols), return_daily
        )
        analytics = strategy_analytics + comparator_analytics + asset_analytics

        asset_weights = FicaDataFrameConverter.df_to_asset_weights(signals, Frequency.monthly)
        return analytics, asset_weights


# noinspection PyAttributeOutsideInit
class Effect(Strategy):
    def __init__(self, carry_type: Union[str, CarryType], closing_threshold: float, cost: float,
                 day_of_week: Union[int, DayOfWeek], frequency: Union[str, Frequency], include_shorts: bool,
                 inflation_lag_in_months: int, interest_rate_cut_off_long: float, interest_rate_cut_off_short: float,
                 moving_average_long_term: int, moving_average_short_term: int, is_realtime_inflation_forecast: bool,
                 trend_indicator: Union[str, TrendIndicator]) -> None:
        """Effect class to hold data from database"""
        super().__init__(Name.effect)
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
    def __init__(
            self, model: str, signal: str, currency: str, response_function: bool,
            exposure: float, momentum_weights: List[float], transaction_cost: float
    ) -> None:
        super().__init__(Name.fx)
        self.model = model
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
        self.defensive = None
        self.asset_inputs = []
        self.carry_assets = []
        self.spot_assets = []

    @property
    def defensive(self) -> bool:
        return self._defensive

    @defensive.setter
    def defensive(self, x: bool) -> None:
        self._defensive = x

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
        spot, carry, cash, ppp = fxmodels.format_data(self)
        signal, volatility = fxmodels.calculate_signals(self, spot, carry, cash, ppp)
        exposure, exposure_agg = fxmodels.determine_sizing(self, signal, volatility)
        returns, contribution, carry_base = fxmodels.calculate_returns(self, carry, signal, exposure, exposure_agg)

        asset_analytics = FxDataFrameConverter.create_asset_analytics(contribution)
        asset_weights = FxDataFrameConverter.df_to_asset_weights(exposure, Frequency.monthly)
        strategy_analytics = FxDataFrameConverter.create_strategy_analytics(
            returns['returns'], returns['returns_cum'], returns['returns_net_cum'], returns['strength_of_signal']
        )
        analytics = asset_analytics + strategy_analytics
        return analytics, asset_weights


# noinspection PyAttributeOutsideInit
class Maven(Strategy):
    def __init__(
            self, er_tr: str, frequency: Union[str, Frequency], day_of_week: Union[int, DayOfWeek],
            business_tstzrange: DateTimeTZRange, asset_count: int, long_cutoff: int, short_cutoff: int,
            val_period_months: int, val_period_base: int, momentum_weights: List[float], volatility_weights: List[float]
    ):
        super().__init__(Name.maven)
        self.er_tr = er_tr
        self.frequency = frequency
        self.day_of_week = day_of_week
        self.business_tstzrange = business_tstzrange
        self.asset_count = asset_count
        self.long_cutoff = long_cutoff
        self.short_cutoff = short_cutoff
        self.val_period_months = val_period_months
        self.val_period_base = val_period_base
        self.momentum_weights = momentum_weights
        self.volatility_weights = volatility_weights
        self.asset_inputs = []

    @property
    def er_tr(self) -> str:
        return self._er_tr

    @er_tr.setter
    def er_tr(self, x: str) -> None:
        self._er_tr = x

    @property
    def frequency(self) -> Frequency:
        return self._frequency

    @frequency.setter
    def frequency(self, x: Union[str, Frequency]) -> None:
        self._frequency = x if isinstance(x, Frequency) else Frequency[x]

    @property
    def day_of_week(self) -> DayOfWeek:
        return self._day_of_week

    @day_of_week.setter
    def day_of_week(self, x: Union[int, DayOfWeek]) -> None:
        self._day_of_week = x if isinstance(x, DayOfWeek) else DayOfWeek(x)

    @property
    def business_tstzrange(self) -> DateTimeTZRange:
        return self._business_tstzrange

    @business_tstzrange.setter
    def business_tstzrange(self, x: DateTimeTZRange) -> None:
        self._business_tstzrange = x

    @property
    def asset_count(self) -> int:
        return self._asset_count

    @asset_count.setter
    def asset_count(self, x: int) -> None:
        self._asset_count = x

    @property
    def long_cutoff(self) -> int:
        return self._long_cutoff

    @long_cutoff.setter
    def long_cutoff(self, x: int) -> None:
        self._long_cutoff = x

    @property
    def short_cutoff(self) -> int:
        return self._short_cutoff

    @short_cutoff.setter
    def short_cutoff(self, x: int) -> None:
        self._short_cutoff = x

    @property
    def val_period_months(self) -> int:
        return self._val_period_months

    @val_period_months.setter
    def val_period_months(self, x: int) -> None:
        self._val_period_months = x

    @property
    def val_period_base(self) -> int:
        return self._val_period_base

    @val_period_base.setter
    def val_period_base(self, x: int) -> None:
        self._val_period_base = x

    @property
    def momentum_weights(self) -> List[float]:
        return self._momentum_weights

    @momentum_weights.setter
    def momentum_weights(self, x: List[float]) -> None:
        self._momentum_weights = x

    @property
    def volatility_weights(self) -> List[float]:
        return self._volatility_weights

    @volatility_weights.setter
    def volatility_weights(self, x: List[float]) -> None:
        self._volatility_weights = x

    @property
    def asset_inputs(self) -> List[MavenAssetInput]:
        return self._asset_inputs

    @asset_inputs.setter
    def asset_inputs(self, x: List[MavenAssetInput]) -> None:
        self._asset_inputs = x

    def run(self) -> Tuple[List[FundStrategyAnalytic], List[FundStrategyAssetWeight]]:
        asset_returns = maven.format_data(self)
        maven_returns = maven.calculate_excess_returns(self, asset_returns)
        momentum, value, long_signals, short_signals, volatility = maven.calculate_signals(self, maven_returns)
        returns, asset_contribution_long, asset_contribution_short = \
            maven.run_performance_stats(self, maven_returns, volatility, long_signals, short_signals)

        asset_contributions = maven.contributions_to_weights(asset_contribution_short, asset_contribution_long)

        asset_analytics = MavenDataFrameConverter.create_asset_analytics(value, momentum, self.frequency)
        asset_weights = MavenDataFrameConverter.df_to_asset_weights(asset_contributions, self.frequency)
        strategy_analytics = MavenDataFrameConverter.create_strategy_analytics(
            returns['equal notional'], returns['equal volatility'], returns['maven long gross'],
            returns['maven short gross'], returns['maven long net'], returns['maven short net'], self.frequency
        )
        analytics = asset_analytics + strategy_analytics
        return analytics, asset_weights