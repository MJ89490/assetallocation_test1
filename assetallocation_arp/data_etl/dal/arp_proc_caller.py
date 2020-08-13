from typing import List, Union, Optional
from decimal import Decimal
from datetime import datetime
from os import environ
from json import loads

from assetallocation_arp.data_etl.dal.db import Db
from assetallocation_arp.data_etl.dal.data_models.strategy import Times
from assetallocation_arp.data_etl.dal.data_models.asset_analytic import AssetAnalytic
from assetallocation_arp.data_etl.dal.data_models.fund_strategy import (FundStrategy, FundStrategyAssetAnalytic,
                                                                        FundStrategyAssetWeight)
from assetallocation_arp.data_etl.dal.type_converter import DbTypeConverter
from assetallocation_arp.data_etl.dal.data_models.asset import TimesAsset
from assetallocation_arp.common_enums.strategy import Name


class ArpProcCaller(Db):
    def __init__(self):
        config = loads(environ.get('DATABASE', '{}'))
        user = config.get('USER')
        password = config.get('PASSWORD')
        host = config.get('HOST')
        port = config.get('PORT')
        database = config.get('DATABASE')

        super().__init__(f'postgresql://{user}:{password}@{host}:{port}/{database}')

    def insert_times(self, times: Times, user_id: str) -> int:
        t_version = self._insert_times_strategy(times, user_id)
        if times.assets:
            self._insert_times_assets(t_version, times.assets)

        return t_version

    def select_times(self, times_version) -> Optional[Times]:
        times = self._select_times_strategy(times_version)

        if times is not None:
            times.assets = self._select_times_assets(times_version)

        return times

    def select_times_with_asset_analytics(self, times_version, business_datetime) -> Optional[Times]:
        times = self._select_times_strategy(times_version)

        if times is not None:
            times.assets = self._select_times_assets_with_analytics(times_version, business_datetime)

        return times

    def _insert_times_strategy(self, times: Times, user_id: str) -> int:
        res = self.call_proc('arp.insert_times_strategy',
                             [times.description, user_id, times.time_lag_interval, times.leverage_type.name,
                              times.volatility_window, times.short_signals, times.long_signals, times.frequency.name,
                              times.day_of_week.value])

        return res[0]['t_version']

    def _select_times_strategy(self, times_version) -> Optional[Times]:
        res = self.call_proc('arp.select_times_strategy', [times_version])
        if not res:
            return

        row = res[0]
        t = Times(row['day_of_week'], row['frequency'], row['leverage_type'], row['long_signals'], row['short_signals'],
                  -DbTypeConverter.month_interval_to_int(row['time_lag']), row['volatility_window'])
        t.version = times_version
        t.description = row['description']
        return t

    def _insert_times_assets(self, times_version: int, times_assets: List[TimesAsset]) -> bool:
        times_assets = self._times_assets_to_composite(times_assets)
        res = self.call_proc('arp.insert_times_assets', [times_version, times_assets])
        asset_ids = res[0].get('asset_ids')
        return bool(asset_ids)

    def _select_times_assets_with_analytics(self, times_version, business_datetime) -> Optional[List[TimesAsset]]:
        res = self.call_proc('arp.select_times_assets_with_analytics', [times_version, business_datetime])

        if not res:
            return

        times_assets = []
        for r in res:
            t = TimesAsset(r['ticker'], r['category'], r['country'], r['currency'], r['name'], r['asset_type'],
                           r['s_leverage'], r['signal_ticker'], r['future_ticker'], r['cost'])
            t.description = r['description']
            t.is_tr = r['is_tr']

            # asset_analytics is a str of the format '{"(source1,category1,value1)",..."(sourceN,categoryN,valueN)"}'
            for i in r['asset_analytics'][2:-2].split('","'):
                source, category, value = (i[1: -1].split(','))
                value = Decimal(value)

                t.add_analytic(AssetAnalytic(r['ticker'], source, category, value))

            times_assets.append(t)

        return times_assets

    def _select_times_assets(self, times_version) -> Optional[List[TimesAsset]]:
        res = self.call_proc('arp.select_times_assets', [times_version])

        if not res:
            return

        times_assets = []
        for r in res:
            t = TimesAsset(r['ticker'], r['category'], r['country'], r['currency'], r['name'], r['asset_type'],
                           r['s_leverage'], r['signal_ticker'], r['future_ticker'], r['cost'])
            t.description = r['description']
            t.is_tr = r['is_tr']

            times_assets.append(t)

        return times_assets

    def insert_fund_strategy_results(self, fund_strategy: FundStrategy, user_id: str) -> bool:
        ticker_weights = self._weights_to_composite(fund_strategy.asset_weights)
        ticker_analytics = self._analytics_to_composite(fund_strategy.asset_analytics)

        res = self.call_proc('arp.insert_fund_strategy_results',
                             [fund_strategy.business_datetime, fund_strategy.fund_name, fund_strategy.output_is_saved,
                              fund_strategy.strategy_name.name, fund_strategy.strategy_version, fund_strategy.weight,
                              user_id, fund_strategy.python_code_version, ticker_weights, ticker_analytics])
        fund_strategy_id = res[0].get('fund_strategy_id')

        return fund_strategy_id is not None

    @staticmethod
    def _times_assets_to_composite(times_assets: List[TimesAsset]) -> List[str]:
        """Format to match database type asset.times_asset[]"""
        return [f'("{i.category.name}","{i.country.name}","{i.currency.name}","{i.description}","{i.name}",' 
                f'"{i.ticker}","{"t" if i.is_tr else "f"}","{i.type}","{i.signal_ticker}","{i.future_ticker}",' 
                f'{i.cost},{i.s_leverage})' for i in times_assets]

    @staticmethod
    def _analytics_to_composite(analytics: List[FundStrategyAssetAnalytic]) -> List[str]:
        """Format to match database type arp.ticker_category_subcategory_value[]"""
        return [f'("{i.asset_ticker}","{i.category}","{i.subcategory}",{i.value})' for i in analytics]

    @staticmethod
    def _weights_to_composite(weights: List[FundStrategyAssetWeight]) -> List[str]:
        """Format to match database type arp.ticker_weight_weight[]"""
        return [f'("{i.asset_ticker}",{i.strategy_weight},{i.implemented_weight})' for i in weights]

    def select_fund_strategy_results(self, fund_name: str, strategy_name: Union[str, Name],
                                     business_datetime: datetime = datetime.today(),
                                     system_datetime: datetime = datetime.today()) -> Optional[FundStrategy]:
        strategy_name = strategy_name.name if isinstance(strategy_name, Name) else Name[strategy_name].name

        res = self.call_proc('arp.select_fund_strategy_results',
                             [fund_name, strategy_name, business_datetime, system_datetime])

        if not res:
            return

        fund_strategy = FundStrategy(fund_name, strategy_name, res[0]['strategy_version'], res[0]['weight'])
        fund_strategy.business_datetime = res[0]['business_datetime']
        fund_strategy.output_is_saved = res[0]['output_is_saved']
        fund_strategy.python_code_version = res[0]['python_code_version']

        for row in res:
            aw = FundStrategyAssetWeight(row['asset_ticker'], row['strategy_weight'])
            aw.implemented_weight = row['implemented_weight']
            fund_strategy.add_fund_strategy_asset_weight(aw)

            # asset_analytics is a str of the format
            # '{"(category1,subcategory1,valu1e)",..."(categoryN,subcategoryN,valueN)"}'
            for i in row['asset_analytics'][2:-2].split('","'):
                category, subcategory, value = (i[1: -1].split(','))
                value = Decimal(value)
                fund_strategy.add_fund_strategy_asset_analytic(
                    FundStrategyAssetAnalytic(row['asset_ticker'], category, subcategory, value))

        return fund_strategy


if __name__ == '__main__':
    from datetime import datetime

    d = ArpProcCaller()

    t = Times(0, 'weekly', 'e', [], [], 0, 0)
    t_v = d._insert_times_strategy(t, 'JS89275', [])

    ta1 = TimesAsset('test_ticker1', 'Equity', 'US', 'EUR', 'test_name', 'b', 2, 'f', 'g', Decimal(1))
    ta2 = TimesAsset('test_ticker1', 'FX', 'US', 'EUR', 'test_name', 'b', 2, 'f', 'g', Decimal(1))

    ins = d._insert_times_assets(t_v, [ta1])
    print(ins)

    ins = d._insert_times_assets(t_v, [ta2])
    print(ins)