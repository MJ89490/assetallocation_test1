from typing import List
from datetime import datetime, date

from assetallocation_arp.data_etl.dal.data_models.fund_strategy import (FundStrategyAssetAnalytic,
                                                                        FundStrategyAssetWeight)
from assetallocation_arp.data_etl.dal.data_models.asset import TimesAssetInput, EffectAsset, AssetAnalytic


class DbTypeConverter:
    """Convert between python and postgres types"""
    @staticmethod
    def month_interval_to_int(month_interval: str) -> int:
        return int(month_interval[:-5])

    @staticmethod
    def month_lag_int_to_interval(month_lag: int) -> str:
        return f'{-month_lag} mons'


class ArpTypeConverter(DbTypeConverter):
    """Convert between python and ARP database types"""
    @staticmethod
    def times_assets_to_composite(times_assets: List[TimesAssetInput]) -> List[str]:
        """Format to match database type arp.ticker_ticker_cost_leverage[]"""
        return [f'("{i.signal_ticker}","{i.future_ticker}","{i.cost}","{i.s_leverage}")' for i in times_assets]

    @staticmethod
    def analytics_to_composite(analytics: List[FundStrategyAssetAnalytic]) -> List[str]:
        """Format to match database type arp.ticker_date_category_subcategory_value[]"""
        return [f'("{i.asset_ticker}","{i.business_date}","{i.category.name}","{i.subcategory.name}",{i.value})' for i in analytics]

    @staticmethod
    def weights_to_composite(weights: List[FundStrategyAssetWeight]) -> List[str]:
        """Format to match database type arp.ticker_date_weight_weight[]"""
        return [f'("{i.asset_ticker}","{i.business_date}",{i.strategy_weight},{i.implemented_weight})' for i in weights]

    @staticmethod
    def effect_assets_to_composite(effect_assets: List[EffectAsset]) -> List[str]:
        """Format to match database type asset.effect_asset[]"""
        pass  # TODO add database type asset.effect_asset

    @staticmethod
    def asset_analytics_str_to_objects(asset_ticker: str, asset_analytics_str: str) -> List[AssetAnalytic]:
        """asset_analytics is a str of the format
        '{"(category1,business_datetime1,value1)",..."(categoryN,business_datetimeN,valueN)"}'
        """
        asset_analytics = []
        for i in asset_analytics_str[2:-2].split('","'):
            category, business_datetime, value = (i[1: -1].split(','))
            business_datetime = datetime.strptime(business_datetime, '\\"%Y-%m-%d %H:%M:%S+00\\"')
            value = float(value)

            asset_analytics.append(AssetAnalytic(asset_ticker, category, business_datetime, value))

        return asset_analytics

    @staticmethod
    def fund_strategy_asset_analytics_str_to_objects(asset_ticker: str, business_date: date,
                                                     asset_analytics_str: str) -> List[FundStrategyAssetAnalytic]:
        """asset_analytics is a str of the format
        '{"(category1,subcategory1,value1)",..."(categoryN,subcategoryN,valueN)"}'
        """
        asset_analytics = []
        for i in asset_analytics_str[2:-2].split('","'):
            category, subcategory, value = (j.strip('\\"') for j in i[1: -1].split(','))
            value = float(value)
            asset_analytics.append(FundStrategyAssetAnalytic(asset_ticker, business_date, category, subcategory, value))

        return asset_analytics
