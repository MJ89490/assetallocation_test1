from typing import List
from datetime import datetime, date

from assetallocation_arp.data_etl.dal.data_models.fund_strategy import (FundStrategyAssetAnalytic, FundStrategyAnalytic,
                                                                        FundStrategyAssetWeight)
from assetallocation_arp.data_etl.dal.data_models.asset import TimesAssetInput, EffectAssetInput, AssetAnalytic, \
    FxAssetInput, MavenAssetInput
from assetallocation_arp.common_libraries.dal_enums.fund_strategy import AggregationLevel


class DbTypeConverter:
    """Convert between python and postgres types"""
    @staticmethod
    def month_interval_to_int(month_interval: str) -> int:
        return int(month_interval[:-5])

    @staticmethod
    def month_lag_int_to_interval(month_lag: int) -> str:
        return f'{-month_lag} mons'

    @staticmethod
    def to_composite(*args) -> str:
        """Return composite string"""
        elements = []
        for i in args:
            if isinstance(i, str) or isinstance(i, date):
                elements.append(f'"{i}"')
            elif i is None:
                elements.append('')
            else:
                elements.append(str(i))

        return '(' + ','.join(elements) + ')'

    @staticmethod
    def from_composite(composite: str) -> List:
        """split composite string into str, datetime and float arguments"""
        res = []
        for i in composite[1: -1].split(','):
            if i.startswith(('"', '\\"')):
                i = i.strip('\\"').strip('"')
                try:
                    res.append(datetime.strptime(i, '%Y-%m-%d %H:%M:%S+00'))
                except ValueError:
                    res.append(i)
            else:
                try:
                    res.append(float(i))
                except ValueError:
                    res.append(i)

        return res


class ArpTypeConverter(DbTypeConverter):
    """Convert between python and ARP database types"""
    @staticmethod
    def times_assets_to_composite(times_assets: List[TimesAssetInput]) -> List[str]:
        """Format to match database type arp.asset_ticker_ticker_cost_leverage[]"""
        return [
            DbTypeConverter.to_composite(i.asset_subcategory.name, i.signal_ticker, i.future_ticker, i.cost, i.s_leverage)
            for i in times_assets
        ]

    @staticmethod
    def maven_assets_to_composite(maven_assets: List[MavenAssetInput]) -> List[str]:
        """Format to match database type
        arp.ticker_ticker_ticker_subcategory_description_currency_class_excess_weight_cost[]
        """
        return [
            DbTypeConverter.to_composite(
                i.bbg_tr_ticker, i.bbg_er_ticker, i.cash_ticker, i.asset_subcategory, i.description, i.currency,
                i.asset_class, i.true_excess, i.asset_weight, i.transaction_cost
            ) for i in maven_assets
        ]

    @staticmethod
    def fx_assets_to_composite(fx_assets: List[FxAssetInput]) -> List[str]:
        """Format to match database type arp.ticker_ticker_cost_leverage[]"""
        return [DbTypeConverter.to_composite(i.ppp_ticker, i.cash_rate_ticker, i.currency) for i in fx_assets]

    @staticmethod
    def analytics_to_composite(analytics: List[FundStrategyAnalytic]) -> List[str]:
        """Format to match database type arp.asset_date_aggregation_category_subcategory_frequency_value[]"""
        return [DbTypeConverter.to_composite(
            getattr(i, "asset_subcategory", None), i.business_date, i.aggregation_level.name, i.category.name,
            i.subcategory.name, i.frequency.name, i.value
        )for i in analytics]

    @staticmethod
    def weights_to_composite(weights: List[FundStrategyAssetWeight]) -> List[str]:
        """Format to match database type arp.asset_date_frequency_weight_weight[]"""
        return [DbTypeConverter.to_composite(
            i.asset_subcategory, i.business_date, i.frequency.name, i.strategy_weight, i.implemented_weight
        ) for i in weights]

    @staticmethod
    def effect_assets_to_composite(effect_assets: List[EffectAssetInput]) -> List[str]:
        """Format to match database type arp.ticker_code_code_size[]"""
        return [DbTypeConverter.to_composite(i.ticker, i.ndf_code, i.spot_code, i.position_size) for i in effect_assets]

    @staticmethod
    def asset_analytics_str_to_objects(asset_ticker: str, asset_analytics_str: str) -> List[AssetAnalytic]:
        """asset_analytics is a str of the format
        '{"(category1,business_datetime1,value1)",..."(categoryN,business_datetimeN,valueN)"}'
        """
        asset_analytics = []
        for i in asset_analytics_str[2:-2].split('","'):
            category, business_datetime, value = DbTypeConverter.from_composite(i)
            asset_analytics.append(AssetAnalytic(asset_ticker, category, business_datetime, value))

        return asset_analytics

    @staticmethod
    def fund_strategy_analytics_str_to_objects(
            asset_subcategory: str, business_date: date, asset_analytics_str: str
    ) -> List[FundStrategyAnalytic]:
        """analytics is a str of the format aggregation_category_subcategory_frequency_value
        '{"(aggregation_level1,category1,subcategory1,frequency1,value1)",...
        "(aggregation_levelN,categoryN,subcategoryN,frequencyN,valueN)"}'
        """
        analytics = []
        for i in asset_analytics_str[2:-2].split('","'):
            aggregation_level, category, subcategory, frequency, value = DbTypeConverter.from_composite(i)
            if aggregation_level == AggregationLevel.asset.name:
                a = FundStrategyAssetAnalytic(asset_subcategory, business_date, category, subcategory, value, frequency)
            else:
                a = FundStrategyAnalytic(business_date, category, subcategory, value, frequency, aggregation_level)
            analytics.append(a)

        return analytics
