from typing import List, Union, Optional
from decimal import Decimal
from datetime import datetime
from os import environ
from json import loads

from assetallocation_arp.data_etl.dal.db import Db
from assetallocation_arp.data_etl.dal.strategy import Times
from data_etl.dal.asset_analytic import AssetAnalytic
from assetallocation_arp.data_etl.dal.fundstrategy import (FundStrategy, FundStrategyAssetAnalytic,
                                                           FundStrategyAssetWeight)
from assetallocation_arp.data_etl.dal.type_converter import month_interval_to_int
from assetallocation_arp.data_etl.dal.asset import TimesAsset
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

    def insert_times_strategy(self, times: Times, user_id: str, asset_tickers: List[str]) -> int:
        res = self.call_proc('arp.insert_times_strategy',
                             [times.description, user_id, times.time_lag_interval, times.leverage_type.name,
                              times.volatility_window, times.short_signals, times.long_signals, times.frequency.name,
                              times.day_of_week.value, asset_tickers])
        return res[0]['t_version']

    def select_times_strategy(self, times_version) -> Optional[Times]:
        res = self.call_proc('arp.select_times_strategy', [times_version])
        if not res:
            return

        row = res[0]
        t = Times(row['day_of_week'], row['frequency'], row['leverage_type'], row['long_signals'], row['short_signals'],
                  -month_interval_to_int(row['time_lag']), row['volatility_window'])
        t.version = times_version
        t.description = row['description']
        return t

    def select_times_assets(self, times_version, business_datetime) -> Optional[List[TimesAsset]]:
        res = self.call_proc('arp.select_times_assets', [times_version, business_datetime])

        if not res:
            return

        times_assets = []
        for r in res:
            t = TimesAsset(r['ticker'], r['category'], r['country'], r['currency'], r['name'], r['asset_type'],
                           r['s_leverage'], r['signal_ticker'], r['future_ticker'], r['cost'])
            t.description = r['description']

            # asset_analytics is a str of the format '{"(source1,category1,value1)",..."(sourceN,categoryN,valueN)"}'
            for i in r['asset_analytics'][2:-2].split('","'):
                source, category, value = (i[1: -1].split(','))
                value = Decimal(value)

                t.add_analytic(AssetAnalytic(r['ticker'], source, category, value))

            times_assets.append(t)

        return times_assets

    def insert_fund_strategy_results(self, fund_strategy: FundStrategy, user_id: str) -> bool:
        ticker_weights = self._weights_to_composite(fund_strategy.asset_weights)
        ticker_analytics = self._analytics_to_composite(fund_strategy.asset_analytics)

        res = self.call_proc('arp.insert_fund_strategy_results',
                                          [fund_strategy.business_datetime, fund_strategy.fund_name,
                                           fund_strategy.output_is_saved, fund_strategy.strategy_name.name,
                                           fund_strategy.strategy_version, fund_strategy.weight, user_id,
                                           fund_strategy.python_code_version, ticker_weights, ticker_analytics])
        fund_strategy_id = res[0].get('fund_strategy_id')

        return fund_strategy_id is not None

    @staticmethod
    def _analytics_to_composite(analytics: List[FundStrategyAssetAnalytic]):
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

    # d.select_times_strategy(1)
    # ta = d.select_times_assets(1, datetime(2020, 1, 2))
    # print(ta)
    # for i in ta:
    #     for j in i.asset_analytics:
    #         print(j.asset_ticker, j.source, j.category, j.value)

    # fs = d.select_fund_strategy_results('f1', 'times')
    #
    # print(fs)

    # fs2 = d.insert_fund_strategy_results(fs, 'JS89275')
    # print(fs2)
    #
    fs = FundStrategy('f1', 'times', 1, Decimal(1))
    u_id = 'JS89275'
    a_ws = [FundStrategyAssetWeight('a1', Decimal(1)), FundStrategyAssetWeight('a2', Decimal(2))]
    a_as = [FundStrategyAssetAnalytic('a1', 'performance', 'spot', Decimal(1)),
            FundStrategyAssetAnalytic('a1', 'signal', 'value', Decimal(2)),
            FundStrategyAssetAnalytic('a2', 'performance', 'spot', Decimal(3)),
            FundStrategyAssetAnalytic('a2', 'signal', 'value', Decimal(4))]
    pcv = '0.0'
    fsr = d.insert_fund_strategy_results(fs, u_id)
    print(fsr)
