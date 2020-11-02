from typing import List, Union, Dict

import pandas as pd

from assetallocation_arp.data_etl.dal.data_models.asset import Asset, TimesAssetInput
from assetallocation_arp.data_etl.dal.data_models.asset_analytic import AssetAnalytic
from assetallocation_arp.common_libraries.dal_enums.fund_strategy import Category, Signal, Performance, AggregationLevel
from assetallocation_arp.common_libraries.dal_enums.strategy import Frequency
from assetallocation_arp.data_etl.dal.data_models.fund_strategy import FundStrategyAssetAnalytic, FundStrategyAssetWeight, FundStrategyAnalytic


class DataFrameConverter:
    @staticmethod
    def assets_to_df(assets: List[Asset]) -> pd.DataFrame:
        asset_analytics = [j for i in assets for j in i.asset_analytics]
        return DataFrameConverter.asset_analytics_to_df(asset_analytics)

    @staticmethod
    def asset_analytics_to_df(asset_analytics: List[AssetAnalytic]) -> pd.DataFrame:
        """DataFrame with index of dates and columns named after tickers"""
        data = [[i.asset_ticker, i.business_datetime, i.value] for i in asset_analytics]
        df = pd.DataFrame(data, columns=['ticker', 'business_datetime', 'value'])
        df = df.drop_duplicates()
        df = df.pivot(index='business_datetime', columns='ticker', values='value')
        df.index = pd.DatetimeIndex(df.index)
        return df

    @staticmethod
    def times_asset_inputs_to_df(asset_inputs: List[TimesAssetInput]) -> pd.DataFrame:
        data = [[i.signal_ticker, i.future_ticker, i.cost, i.s_leverage] for i in asset_inputs]
        return pd.DataFrame(data, columns=['signal_ticker', 'future_ticker', 'cost', 's_leverage'])

    @staticmethod
    def fund_strategy_asset_weights_to_df(assets: List[Asset], asset_weights: List[FundStrategyAssetWeight]) -> pd.DataFrame:
        asset_data = [[i.ticker, i.subcategory] for i in assets]
        asset_df = pd.DataFrame(asset_data, columns=['ticker', 'asset_subcategory'])

        data = [[i.asset_ticker, i.business_date, i.strategy_weight] for i in asset_weights]
        df = pd.DataFrame(data, columns=['ticker', 'business_date', 'value'])

        df = df.merge(asset_df, on='ticker', how='left')
        df = df.set_index(['business_date', 'asset_subcategory', 'ticker']).unstack(['ticker', 'asset_subcategory'])
        df.columns = df.columns.droplevel([0, 1])

        return df

    @staticmethod
    def fund_strategy_asset_analytics_to_df(assets: List[Asset], asset_analytics: List[FundStrategyAssetAnalytic]) -> pd.DataFrame:
        asset_data = [[i.ticker, i.subcategory] for i in assets]
        asset_df = pd.DataFrame(asset_data, columns=['ticker', 'asset_subcategory'])

        data = [[i.asset_ticker, i.business_date, i.subcategory, i.value] for i in asset_analytics]
        df = pd.DataFrame(data, columns=['ticker', 'business_date', 'analytic_subcategory', 'value'])

        df = df.merge(asset_df, on='ticker', how='left')
        df = df.set_index(['business_date', 'analytic_subcategory', 'asset_subcategory', 'ticker']).unstack(['ticker', 'asset_subcategory'])
        df.columns = df.columns.droplevel(0)
        return df

    @staticmethod
    def df_to_asset_analytics(
            analytics: pd.DataFrame, category: Union[str, Category], subcategory: Union[str, Performance, Signal],
            frequency: Union[None, str, Frequency] = None
    ) -> List[FundStrategyAssetAnalytic]:
        """Transform DataFrame with index of business_date and columns of asset tickers to list of
        FundStrategyAssetAnalytics
        """
        return [FundStrategyAssetAnalytic(ticker, index, category, subcategory, float(val), frequency) for ticker, data
                in analytics.items() for index, val in data.iteritems()]

    @staticmethod
    def series_to_strategy_analytics(
            analytics: pd.Series, category: Union[str, Category], subcategory: Union[str, Performance, Signal],
            frequency: Union[None, str, Frequency] = None, aggregation_level: Union[None, str, AggregationLevel] = None
    ) -> List[FundStrategyAnalytic]:
        """Transform Series with index of business_date and to list of FundStrategyAnalytics"""
        return [FundStrategyAnalytic(index, category, subcategory, float(val), frequency, aggregation_level) for
                index, val in analytics.iteritems()]

    @staticmethod
    def df_to_asset_weights(
            weights: pd.DataFrame, frequency: Union[str, Frequency]
    ) -> List[FundStrategyAssetWeight]:
        """Transform DataFrame with index of business_date and columns of asset tickers to list of FundStrategyAssetWeights
        """
        return [FundStrategyAssetWeight(ticker, index, float(val), frequency) for ticker, data in weights.items()
                for index, val in data.iteritems()]


class TimesDataFrameConverter(DataFrameConverter):
    @classmethod
    def create_asset_analytics(cls, signals: pd.DataFrame, returns: pd.DataFrame,
                               r: pd.DataFrame, signals_freqency: Frequency) -> List[FundStrategyAssetAnalytic]:
        """
        :param signals: columns named after tickers, index of dates
        :param returns: columns named after tickers, index of dates
        :param r: columns named after tickers, index of dates
        :return:
        """
        asset_analytics = []

        asset_analytics.extend(cls.df_to_asset_analytics(signals, Category.signal, Signal.momentum, signals_freqency))
        asset_analytics.extend(cls.df_to_asset_analytics(returns, Category.performance, Performance["excess return"], Frequency.daily))
        asset_analytics.extend(cls.df_to_asset_analytics(r, Category.performance, Performance["excess return index"], Frequency.daily))

        return asset_analytics


class FicaDataFrameConverter(DataFrameConverter):
    @classmethod
    def create_asset_analytics(
            cls, carry_roll: pd.DataFrame, cum_contribution: pd.DataFrame, returns: pd.DataFrame,
            carry_daily: pd.DataFrame, return_daily: pd.DataFrame, tickers: List[str]
    ) -> List[FundStrategyAssetAnalytic]:
        """
        :param carry_roll: columns named after countries, index of dates
        :param cum_contribution: columns named after countries, index of dates
        :param returns: columns named after countries, index of dates
        :param carry_daily: columns named after countries, index of dates
        :param return_daily: columns named after countries, index of dates
        :param tickers: ordered list to rename country columns with
        :return:
        """
        analytics = []
        carry_roll.columns = tickers
        cum_contribution.columns = tickers
        returns.columns = tickers
        carry_daily.columns = tickers
        return_daily.columns = tickers

        analytics.extend(cls.df_to_asset_analytics(carry_roll, Category.signal, Signal.carry, Frequency.monthly))
        analytics.extend(cls.df_to_asset_analytics(cum_contribution, Category.performance, Performance['total return'], Frequency.monthly))
        analytics.extend(cls.df_to_asset_analytics(return_daily, Category.Performance, Performance['total return'], Frequency.daily))
        analytics.extend(cls.df_to_asset_analytics(returns, Category.performance, Performance["excess return"]))
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
