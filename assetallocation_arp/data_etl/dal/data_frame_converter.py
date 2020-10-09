from typing import List, Union

import pandas as pd

from assetallocation_arp.data_etl.dal.data_models.asset import Asset, TimesAssetInput
from assetallocation_arp.data_etl.dal.data_models.asset_analytic import AssetAnalytic
from assetallocation_arp.common_libraries.dal_enums.fund_strategy import Category, Signal, Performance
from assetallocation_arp.data_etl.dal.data_models.fund_strategy import FundStrategyAssetAnalytic, FundStrategyAssetWeight


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
        df.columns = df.columns.droplevel(0)

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
    def df_to_asset_analytics(analytics: pd.DataFrame, category: Union[str, Category],
                              subcategory: Union[str, Performance, Signal]) -> List[FundStrategyAssetAnalytic]:
        """Transform DataFrame with index of business_date and columns of asset tickers to list of
        FundStrategyAssetAnalytics
        """
        return [FundStrategyAssetAnalytic(ticker, index, category, subcategory, float(val)) for ticker, data in
                analytics.items() for index, val in data.iteritems()]

    @staticmethod
    def df_to_asset_weights(positioning: pd.DataFrame) -> List[FundStrategyAssetWeight]:
        """Transform DataFrame with index of business_date and columns of asset tickers to list of FundStrategyAssetWeights
        """
        return [FundStrategyAssetWeight(ticker, index, float(val)) for ticker, data in positioning.items() for index, val in
                data.iteritems()]


class TimesDataFrameConverter(DataFrameConverter):
    @classmethod
    def create_asset_analytics(cls, signals: pd.DataFrame, returns: pd.DataFrame,
                               r: pd.DataFrame) -> List[FundStrategyAssetAnalytic]:
        """
        :param signals: columns named after tickers, index of dates
        :param returns: columns named after tickers, index of dates
        :param r: columns named after tickers, index of dates
        :return:
        """
        asset_analytics = []

        asset_analytics.extend(cls.df_to_asset_analytics(signals, Category.signal, Signal.momentum))
        asset_analytics.extend(cls.df_to_asset_analytics(returns, Category.performance, Performance["excess return"]))
        asset_analytics.extend(cls.df_to_asset_analytics(r, Category.performance, Performance["excess return index"]))

        return asset_analytics


class FicaDataFrameConverter(DataFrameConverter):
    @classmethod
    def create_asset_analytics(cls, carry_roll: pd.DataFrame, country_returns: pd.DataFrame,
                               signals: pd.DataFrame, cum_contribution: pd.DataFrame, returns: pd.DataFrame,
                               carry_daily: pd.DataFrame, return_daily: pd.DataFrame) -> List[FundStrategyAssetAnalytic]:
        """
        :param signals: columns named after tickers, index of dates
        :param returns: columns named after tickers, index of dates
        :param r: columns named after tickers, index of dates
        :return:
        """
        # TODO set category and subcategory depending on Simone's reply
        asset_analytics = []

        asset_analytics.extend(cls.df_to_asset_analytics(carry_roll, Category.signal, Signal.momentum))
        asset_analytics.extend(cls.df_to_asset_analytics(country_returns, Category.performance, Performance["excess return"]))
        asset_analytics.extend(cls.df_to_asset_analytics(signals, Category.performance, Performance["excess return index"]))
        asset_analytics.extend(cls.df_to_asset_analytics(cum_contribution, Category.signal, Signal.momentum))
        asset_analytics.extend(
            cls.df_to_asset_analytics(returns, Category.performance, Performance["excess return"]))
        asset_analytics.extend(
            cls.df_to_asset_analytics(carry_daily, Category.performance, Performance["excess return index"]))
        asset_analytics.extend(cls.df_to_asset_analytics(return_daily, Category.signal, Signal.momentum))

        return asset_analytics
