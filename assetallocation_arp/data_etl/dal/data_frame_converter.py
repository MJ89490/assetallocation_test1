from typing import List

import pandas as pd

from assetallocation_arp.data_etl.dal.data_models.asset import Asset, TimesAssetInput
from assetallocation_arp.data_etl.dal.data_models.asset_analytic import AssetAnalytic


class DataFrameConverter:
    @staticmethod
    def assets_to_dataframe(assets: List[Asset]):
        asset_analytics = [j for i in assets for j in i.asset_analytics]
        return DataFrameConverter.asset_analytics_to_dataframe(asset_analytics)

    @staticmethod
    def asset_analytics_to_dataframe(asset_analytics: List[AssetAnalytic]):
        """DataFrame with index of dates and columns named after tickers"""
        data = [[i.asset_ticker, i.business_datetime, i.value] for i in asset_analytics]
        df = pd.DataFrame(data, columns=['ticker', 'business_datetime', 'value'])
        print(df.head())
        return df.pivot(index='business_datetime', columns='ticker', values='value')

    @staticmethod
    def times_asset_inputs_to_dataframe(asset_inputs: List[TimesAssetInput]):
        data = [[i.signal_ticker, i.future_ticker, i.cost, i.s_leverage] for i in asset_inputs]
        return pd.DataFrame(data, columns=['signal_ticker', 'future_ticker', 'cost', 's_leverage'])