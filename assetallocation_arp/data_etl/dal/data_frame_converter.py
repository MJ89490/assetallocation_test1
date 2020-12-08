from typing import List, Union, Tuple
from itertools import chain

import pandas as pd

from assetallocation_arp.data_etl.dal.data_models.asset import Asset, TimesAssetInput
from assetallocation_arp.data_etl.dal.data_models.asset_analytic import AssetAnalytic
from assetallocation_arp.common_libraries.dal_enums.fund_strategy import Category, Signal, Performance, AggregationLevel
from assetallocation_arp.common_libraries.dal_enums.strategy import Frequency
from assetallocation_arp.data_etl.dal.data_models.fund_strategy import FundStrategyAssetAnalytic, FundStrategyAssetWeight, FundStrategyAnalytic


class DataFrameConverter:
    @staticmethod
    def assets_to_df(assets: List[Tuple[str, Asset]]) -> pd.DataFrame:
        asset_analytics = [(asset_subcategory, j) for asset_subcategory, i in assets for j in i.asset_analytics]
        return DataFrameConverter.asset_analytics_to_df(asset_analytics)

    @staticmethod
    def asset_analytics_to_df(asset_analytics: List[Tuple[str, AssetAnalytic]]) -> pd.DataFrame:
        """DataFrame with index of dates and columns named after labels"""
        data = [[label, i.business_datetime, i.value] for label, i in asset_analytics]
        df = pd.DataFrame(data, columns=['label', 'business_datetime', 'value'])
        df = df.drop_duplicates()
        df = df.pivot(index='business_datetime', columns='label', values='value')
        df.index = pd.DatetimeIndex(df.index)
        return df

    @staticmethod
    def times_asset_inputs_to_df(asset_inputs: List[TimesAssetInput]) -> pd.DataFrame:
        data = [[i.asset_subcategory, i.signal_ticker, i.future_ticker, i.cost, i.s_leverage] for i in asset_inputs]
        return pd.DataFrame(data, columns=['asset_subcategory', 'signal_ticker', 'future_ticker', 'cost', 's_leverage'])

    @staticmethod
    def fund_strategy_asset_weights_to_df( asset_weights: List[FundStrategyAssetWeight]) -> pd.DataFrame:
        data = [[i.asset_subcategory, i.business_date, i.strategy_weight] for i in asset_weights]
        df = pd.DataFrame(data, columns=['asset_subcategory', 'business_date', 'value'])
        df = df.set_index(['business_date', 'asset_subcategory']).unstack(['asset_subcategory'])
        df.columns = df.columns.droplevel(0)
        return df

    @staticmethod
    def fund_strategy_asset_analytics_to_df(asset_analytics: List[FundStrategyAssetAnalytic]) -> pd.DataFrame:
        data = [[i.asset_subcategory, i.business_date, i.subcategory, i.value] for i in asset_analytics]
        df = pd.DataFrame(data, columns=['asset_subcategory', 'business_date', 'analytic_subcategory', 'value'])
        df = df.set_index(['business_date', 'analytic_subcategory', 'asset_subcategory']).unstack(['asset_subcategory'])
        df.columns = df.columns.droplevel(0)
        return df

    @staticmethod
    def df_to_asset_analytics(
            analytics: pd.DataFrame, category: Union[str, Category], subcategory: Union[str, Performance, Signal],
            frequency: Union[None, str, Frequency] = None
    ) -> List[FundStrategyAssetAnalytic]:
        """Transform DataFrame with index of business_date and columns of asset_subcategory to list of
        FundStrategyAssetAnalytics
        """
        return [
            FundStrategyAssetAnalytic(asset_subcategory.name, index, category, subcategory, float(val), frequency)
            for asset_subcategory, data in analytics.items() for index, val in data.iteritems() if pd.notna(val)
        ]

    @staticmethod
    def series_to_strategy_analytics(
            analytics: pd.Series, category: Union[str, Category], subcategory: Union[str, Performance, Signal],
            frequency: Union[None, str, Frequency] = None, aggregation_level: Union[None, str, AggregationLevel] = None
    ) -> List[FundStrategyAnalytic]:
        """Transform Series with index of business_date and to list of FundStrategyAnalytics"""
        return [FundStrategyAnalytic(index, category, subcategory, float(val), frequency, aggregation_level) for
                index, val in analytics.iteritems() if pd.notna(val)]

    @staticmethod
    def df_to_asset_weights(weights: pd.DataFrame, frequency: Union[str, Frequency]) -> List[FundStrategyAssetWeight]:
        """Transform DataFrame with index of business_date and columns of asset_subcategory to list of
        FundStrategyAssetWeights
        """
        return [
            FundStrategyAssetWeight(col.name, index, float(val), frequency) for col, data in weights.items() for index, val
            in data.iteritems() if pd.notna(val)
        ]


class TimesDataFrameConverter(DataFrameConverter):
    @classmethod
    def create_asset_analytics(
            cls, signals: pd.DataFrame, returns: pd.DataFrame, r: pd.DataFrame, signals_frequency: Frequency
    ) -> List[FundStrategyAssetAnalytic]:
        """
        :param signals: columns named after asset_subcategory, index of dates
        :param returns: columns named after asset_subcategory, index of dates
        :param r: columns named after asset_subcategory, index of dates
        :param signals_frequency: frequency of signals
        :return:
        """
        analytics = []

        analytics.extend(cls.df_to_asset_analytics(signals, Category.signal, Signal.momentum, signals_frequency))
        analytics.extend(cls.df_to_asset_analytics(returns, Category.performance, Performance["excess return"], Frequency.daily))
        analytics.extend(cls.df_to_asset_analytics(r, Category.performance, Performance["excess return index"], Frequency.daily))

        return analytics


class FicaDataFrameConverter(DataFrameConverter):
    @classmethod
    def create_asset_analytics(cls, carry_roll: pd.DataFrame, cum_contribution: pd.DataFrame, carry_daily: pd.DataFrame,
                               return_daily: pd.DataFrame) -> List[FundStrategyAssetAnalytic]:
        """
        :param carry_roll: columns named after countries, index of dates
        :param cum_contribution: columns named after countries, index of dates
        :param carry_daily: columns named after countries, index of dates
        :param return_daily: columns named after countries, index of dates
        :return:
        """
        analytics = []

        analytics.extend(cls.df_to_asset_analytics(carry_roll, Category.signal, Signal.carry, Frequency.monthly))
        analytics.extend(cls.df_to_asset_analytics(cum_contribution, Category.performance, Performance['total return'], Frequency.monthly))
        analytics.extend(cls.df_to_asset_analytics(return_daily, Category.Performance, Performance['total return'], Frequency.daily))
        analytics.extend(cls.df_to_asset_analytics(carry_daily, Category.performance, Performance["excess return index"]))

        return analytics

    @classmethod
    def create_strategy_analytics(
            cls, cum_contribution: pd.Series, returns: pd.DataFrame, carry_roll: pd.Series, carry_daily: pd.DataFrame
    ) -> List[FundStrategyAnalytic]:
        """
        :param returns: columns of Costs, Net_Return, Arithmetic, index of dates
        :param cum_contribution: index of dates
        :param carry_roll: index of dates
        :param carry_daily: columns of 'fica_10y_return', 'fica_10y_return%', 'correlation', 'beta', index of dates
        :return:
        """
        analytics = []

        analytics.extend(cls.series_to_strategy_analytics(cum_contribution, Category.Performance, Performance['total return'], Frequency.monthly))
        analytics.extend(cls.series_to_strategy_analytics(returns['Costs'], Category.Performance, Performance.cost, Frequency.monthly))
        analytics.extend(cls.series_to_strategy_analytics(returns['Net_Return'], Category.Performance, Performance['net return'], Frequency.monthly))
        analytics.extend(cls.series_to_strategy_analytics(returns['Arithmetic'], Category.Performance, Performance['net return index'], Frequency.monthly))
        analytics.extend(cls.series_to_strategy_analytics(carry_roll, Category.Signal, Signal.carry, Frequency.daily))
        analytics.extend(cls.series_to_strategy_analytics(carry_daily['fica_10y_return'], Category.Performance, Performance['total return index'], Frequency.daily))
        analytics.extend(cls.series_to_strategy_analytics(carry_daily['fica_10y_return%'], Category.Performance, Performance['total return'], Frequency.daily))
        analytics.extend(cls.series_to_strategy_analytics(carry_daily['correlation'], Category.Performance, Performance.correlation, Frequency.daily))
        analytics.extend(cls.series_to_strategy_analytics(carry_daily['beta'], Category.Performance, Performance.beta, Frequency.daily))

        return analytics

    @classmethod
    def create_comparator_analytics(
            cls, carry_roll: pd.Series, carry_daily: pd.DataFrame
    ) -> List[FundStrategyAnalytic]:
        """
        :param carry_roll: index of dates
        :param carry_daily: columns of 'G3_10y_return', 'G3_10y_return%', index of dates
        :return:
        """
        analytics = []
        analytics.extend(cls.series_to_strategy_analytics(carry_roll, Category.Signal, Signal.carry, Frequency.daily, AggregationLevel.comparator))
        analytics.extend(cls.series_to_strategy_analytics(carry_daily['G3_10y_return'], Category.Performance, Performance['total return index'], Frequency.daily, AggregationLevel.comparator))
        analytics.extend(cls.series_to_strategy_analytics(carry_daily['G3_10y_return%'], Category.Performance, Performance['total return'], Frequency.daily, AggregationLevel.comparator))

        return analytics


class FxDataFrameConverter(DataFrameConverter):
    @classmethod
    def create_asset_analytics(cls, contribution: pd.DataFrame) -> List[FundStrategyAssetAnalytic]:
        """
        :param contribution: columns named after countries, index of dates
        :return:
        """
        return cls.df_to_asset_analytics(contribution, Category.Performance, Performance['total return'], Frequency.monthly)

    @classmethod
    def create_strategy_analytics(
            cls, returns: pd.Series, returns_cum: pd.Series, returns_net_cum: pd.Series, strength_of_signal: pd.Series
    ) -> List[FundStrategyAnalytic]:
        """
        :param returns: index of dates
        :param returns_cum: index of dates
        :param returns_net_cum: index of dates
        :param strength_of_signal: index of dates
        :return:
        """
        analytics = []

        analytics.extend(cls.series_to_strategy_analytics(returns, Category.Performance, Performance['return'], Frequency.monthly))
        analytics.extend(cls.series_to_strategy_analytics(returns_cum, Category.Performance, Performance['return index'], Frequency.monthly))
        analytics.extend(cls.series_to_strategy_analytics(returns_net_cum, Category.Performance, Performance['net return index'], Frequency.monthly))
        analytics.extend(cls.series_to_strategy_analytics(strength_of_signal, Category.Signals, Signal['signal strength'], Frequency.monthly))

        return analytics


class MavenDataFrameConverter(DataFrameConverter):
    @classmethod
    def create_asset_analytics(
            cls, value: pd.DataFrame, momentum: pd.DataFrame, frequency: Frequency
    ) -> List[FundStrategyAssetAnalytic]:
        """
        :param value: columns named after asset subcategory, index of dates
        :param momentum: columns named after asset subcategory, index of dates
        :return:
        """
        analytics = cls.df_to_asset_analytics(value, Category.Signal, Signal.value, frequency)
        analytics.extend(cls.df_to_asset_analytics(momentum, Category.Signal, Signal.momentum, frequency))
        return analytics

    @classmethod
    def create_strategy_analytics(
            cls, notional: pd.Series, volatility: pd.Series, long_gross: pd.Series, short_gross: pd.Series,
            long_net: pd.Series, short_net: pd.Series, frequency: Frequency
    ) -> List[FundStrategyAnalytic]:
        """
        :param notional: index of dates
        :param volatility: index of dates
        :param long_gross: index of dates
        :param short_gross: index of dates
        :param long_net: index of dates
        :param short_net: index of dates
        :param frequency: frequency of analytics
        :return:
        """
        analytics = list(
            chain(
                cls.series_to_strategy_analytics(notional, Category.Performance,
                                                 Performance['equal notional return index'], frequency),
                cls.series_to_strategy_analytics(volatility, Category.Performance,
                                                 Performance['equal volatility return index'], frequency),
                cls.series_to_strategy_analytics(long_gross, Category.Performance,
                                                 Performance['long gross return index'], frequency),
                cls.series_to_strategy_analytics(short_gross, Category.Performance,
                                                 Performance['short gross return index'], frequency),
                cls.series_to_strategy_analytics(long_net, Category.Performance, Performance['long net return index'],
                                                 frequency),
                cls.series_to_strategy_analytics(short_net, Category.Performance, Performance['short net return index'],
                                                 frequency)
            )
        )

        return analytics


class EffectDataFrameConverter(DataFrameConverter):
    @classmethod
    def create_asset_analytics(
            cls, trend: pd.DataFrame, carry: pd.DataFrame, frequency: Frequency
    ) -> List[FundStrategyAssetAnalytic]:
        """
        :param trend: columns named after asset subcategory, index of dates
        :param carry: columns named after asset subcategory, index of dates
        :return:
        """
        # TODO change depending on Simone's input
        analytics = list(
            chain(
                cls.df_to_asset_analytics(trend, Category.Signal, Signal.trend, frequency),
                cls.df_to_asset_analytics(carry, Category.Signal, Signal.carry, frequency)
            )
        )
        return analytics

    @classmethod
    def create_strategy_analytics(
            cls, notional: pd.Series, volatility: pd.Series, long_gross: pd.Series,
            short_gross: pd.Series, frequency: Frequency
    ) -> List[FundStrategyAnalytic]:
        """
        :param notional: index of dates
        :param volatility: index of dates
        :param long_gross: index of dates
        :param short_gross: index of dates
        :param frequency: frequency of analytics
        :return:
        """
        # TODO change depending on Simone's input
        analytics = list(
            chain(
                cls.series_to_strategy_analytics(notional, Category.Performance,
                                                 Performance['total return index incl signals'], frequency),
                cls.series_to_strategy_analytics(volatility, Category.Performance,
                                                 Performance['total return index excl signals'], frequency),
                cls.series_to_strategy_analytics(long_gross, Category.Performance,
                                                 Performance['spot index incl signals'], frequency),
                cls.series_to_strategy_analytics(short_gross, Category.Performance,
                                                 Performance['spot index excl signals'], frequency)
            )
        )

        return analytics
