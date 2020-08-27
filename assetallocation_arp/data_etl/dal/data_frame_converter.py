from typing import List

import pandas as pd

from assetallocation_arp.data_etl.dal.data_models.asset import Asset, TimesAssetInput
from assetallocation_arp.data_etl.dal.data_models.asset_analytic import AssetAnalytic
from assetallocation_arp.data_etl.dal.data_models.fund_strategy import FundStrategyAssetWeight, FundStrategyAssetAnalytic


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
        return df.pivot(index='business_datetime', columns='ticker', values='value')

    @staticmethod
    def times_asset_inputs_to_df(asset_inputs: List[TimesAssetInput]) -> pd.DataFrame:
        data = [[i.signal_ticker, i.future_ticker, i.cost, i.s_leverage] for i in asset_inputs]
        return pd.DataFrame(data, columns=['signal_ticker', 'future_ticker', 'cost', 's_leverage'])

    @staticmethod
    def fund_strategy_asset_weights_to_df(asset_weights: List[FundStrategyAssetWeight]) -> pd.DataFrame:
        # TODO need the asset categories!
        data = [[i.asset_ticker, i.business_date, i.strategy_weight] for i in asset_weights]
        df = pd.DataFrame(data, columns=['ticker', 'business_date', 'value'])
        return df.pivot(index='business_date', columns='ticker', values='value')

    @staticmethod
    def fund_strategy_asset_analytics_to_df(asset_analytics: List[FundStrategyAssetAnalytic]) -> pd.DataFrame:
        # TODO need the asset categories!
        data = [[i.asset_ticker, i.business_date, i.subcategory, i.value] for i in asset_analytics]
        df = pd.DataFrame(data, columns=['ticker', 'business_date', 'subcategory', 'value'])
        df = df.set_index(['business_date', 'subcategory', 'ticker']).unstack('ticker')
        df.columns = df.columns.droplevel(0)
        return df
