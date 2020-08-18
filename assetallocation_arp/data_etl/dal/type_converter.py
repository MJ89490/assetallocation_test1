from typing import List
from decimal import Decimal

from assetallocation_arp.data_etl.dal.data_models.fund_strategy import (FundStrategyAssetAnalytic,
                                                                        FundStrategyAssetWeight)
from assetallocation_arp.data_etl.dal.data_models.asset import TimesAsset, EffectAsset, AssetAnalytic


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
    def times_assets_to_composite(times_assets: List[TimesAsset]) -> List[str]:
        """Format to match database type asset.times_asset[]"""
        return [f'("{i.category.name}","{i.country.name}","{i.currency.name}","{i.description}","{i.name}",'
                f'"{i.ticker}","{"t" if i.is_tr else "f"}","{i.type}","{i.signal_ticker}","{i.future_ticker}",'
                f'{i.cost},{i.s_leverage})' for i in times_assets]

    @staticmethod
    def analytics_to_composite(analytics: List[FundStrategyAssetAnalytic]) -> List[str]:
        """Format to match database type arp.ticker_category_subcategory_value[]"""
        return [f'("{i.asset_ticker}","{i.category}","{i.subcategory}",{i.value})' for i in analytics]

    @staticmethod
    def weights_to_composite(weights: List[FundStrategyAssetWeight]) -> List[str]:
        """Format to match database type arp.ticker_weight_weight[]"""
        return [f'("{i.asset_ticker}",{i.strategy_weight},{i.implemented_weight})' for i in weights]

    @staticmethod
    def effect_assets_to_composite(effect_assets: List[EffectAsset]) -> List[str]:
        """Format to match database type asset.effect_asset[]"""
        pass  # TODO add database type asset.effect_asset

    @staticmethod
    def asset_analytics_str_to_objects(asset_ticker: str, asset_analytics_str: str) -> List[AssetAnalytic]:
        # asset_analytics is a str of the format '{"(source1,category1,value1)",..."(sourceN,categoryN,valueN)"}'
        asset_analytics = []
        for i in asset_analytics_str[2:-2].split('","'):
            source, category, value = (i[1: -1].split(','))
            value = Decimal(value)

            asset_analytics.append(AssetAnalytic(asset_ticker, source, category, value))

        return asset_analytics