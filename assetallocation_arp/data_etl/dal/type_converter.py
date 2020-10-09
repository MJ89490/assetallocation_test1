from typing import List, Tuple
from datetime import datetime, date

from assetallocation_arp.data_etl.dal.data_models.fund_strategy import (FundStrategyAssetAnalytic,
                                                                        FundStrategyAssetWeight)
from assetallocation_arp.data_etl.dal.data_models.asset import TimesAssetInput, EffectAssetInput, AssetAnalytic, FicaAssetInput
from assetallocation_arp.data_etl.dal.data_models.ticker import Ticker


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
    def effect_assets_to_composite(effect_assets: List[EffectAssetInput]) -> List[str]:
        """Format to match database type arp.ticker_code_code_size[]"""
        return [f'("{i.ticker}","{i.ndf_code}","{i.spot_code}",{i.position_size})' for i in effect_assets]

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

    @staticmethod
    def ticker_str_to_object(curve_ticker: str) -> Ticker:
        """curve_ticker is a str of the format
        '("{t.category.name}","{t.mth3}","{t.yr1}","{t.yr2}","{t.yr3}","{t.yr4}","{t.yr5}","{t.yr6}","{t.yr7}",' \
        '"{t.yr8}","{t.yr9}","{t.yr10}","{t.yr15}","{t.yr20}","{t.yr30}")'
        """
        category, mth3, yr1, yr2, yr3, yr4, yr5, yr6, yr7, yr8, yr9, yr10, yr15, yr20, yr30 = (j.strip('\\"') for j in curve_ticker[1: -1].split(','))
        return Ticker(category, mth3, yr1, yr2, yr3, yr4, yr5, yr6, yr7, yr8, yr9, yr10, yr15, yr20, yr30)

    @staticmethod
    def fica_assets_to_composite(fica_assets: List[FicaAssetInput]) -> List[List[str]]:
        """Format sovereign, swap and swap_cr tickers to match database type curve.ticker_months_years[]"""
        asset_tickers, sovereign_tickers, swap_tickers, swap_cr_tickers = [], [], [], []

        for i in fica_assets:
            asset_tickers.append(i.ticker)
            sovereign_tickers.append(ArpTypeConverter._tickers_to_composite(i.sovereign_ticker))
            swap_tickers.append(ArpTypeConverter._tickers_to_composite(i.swap_ticker))
            swap_cr_tickers.append(ArpTypeConverter._tickers_to_composite(i.swap_cr_ticker))

        return [asset_tickers, sovereign_tickers, swap_tickers, swap_cr_tickers]

    @staticmethod
    def _tickers_to_composite(t: Ticker) -> str:
        """Format to match database type curve.ticker_months_years"""
        return f'("{t.category.name}","{t.mth3}","{t.yr1}","{t.yr2}","{t.yr3}","{t.yr4}","{t.yr5}","{t.yr6}","{t.yr7}",' \
               f'"{t.yr8}","{t.yr9}","{t.yr10}","{t.yr15}","{t.yr20}","{t.yr30}")'
