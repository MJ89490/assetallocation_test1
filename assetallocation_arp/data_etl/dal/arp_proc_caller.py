from typing import List, Tuple, Any, Optional
from decimal import Decimal
from datetime import datetime

from assetallocation_arp.data_etl.dal.db import Db
from assetallocation_arp.data_etl.dal.times import Times
from assetallocation_arp.data_etl.dal.asset import Asset
from assetallocation_arp.data_etl.dal.asset_analytic import AssetAnalytic
from assetallocation_arp.data_etl.dal.fund import Fund
from assetallocation_arp.data_etl.dal.fundstrategy import FundStrategy
from assetallocation_arp.data_etl.dal.strategyassetanalytic import StrategyAssetAnalytic
from assetallocation_arp.data_etl.dal.fundstrategyassetweight import FundStrategyAssetWeight


class ArpProcCaller(Db):
    def insert_times_strategy(self, times: Times, user_id, asset_tickers: List[str]) -> int:
        t_version = self.call_proc('arp.insert_times_strategy',
                                   [times.description, user_id, times.time_lag, times.leverage_type,
                                    times.volatility_window, times.short_signals, times.long_signals, times.frequency,
                                    times.day_of_week, asset_tickers])

        return t_version[0]

    def select_times_strategy(self, times_version) -> Times:
        times_strategy = self.call_proc('arp.select_times_strategy', [times_version])[0]
        return Times(**times_strategy)

    def select_times_assets(self, times_version, business_datetime) -> List[Tuple[List[AssetAnalytic], Asset]]:
        assets = self.call_proc('arp.select_times_assets', [times_version, business_datetime])
        return [(self._prep_composite_value(r.pop('asset_analytic'), AssetAnalytic), Asset(**r)) for r in assets]

    def insert_fund_strategy_results(self, fund_name: str, fund_strategy: FundStrategy, strategy_id: int, user_id: str,
                                     python_code_version: str) -> bool:
        asset_weight_tickers, implemented_weights, strategy_weights = self._split_asset_weights(FundStrategy.assets)
        asset_analytic_tickers, analytic_types, analytic_subtypes, analytic_values = self._split_asset_analytics(
            asset_analytics)

        fund_strategy_id = self.call_proc('arp.insert_fund_strategy_results',
                                          [fund_strategy.business_datetime, fund_name, fund_strategy.save_output_flag,
                                           strategy_id, fund_strategy.weight, user_id, python_code_version,
                                           asset_weight_tickers, strategy_weights, implemented_weights,
                                           asset_analytic_tickers, analytic_types, analytic_subtypes, analytic_values])[
            0]

        return fund_strategy_id is not None

    @staticmethod
    def _split_asset_analytics(assets: List[Asset]):
        asset_analytic_tickers, analytic_types, analytic_subtypes, analytic_values = [], [], [], []
        for i in assets:
            for j in i.strategy_asset_analytics:
                asset_analytic_tickers.append(i.ticker)
                analytic_types.append(j.analytic_type)
                analytic_subtypes.append(j.analytic_subtype)
                analytic_values.append(j.value)

        return asset_analytic_tickers, analytic_types, analytic_subtypes, analytic_values

    @staticmethod
    def _split_asset_weights(assets: List[Asset]):
        asset_weight_tickers, strategy_weights, implemented_weights = [], [], []
        for i in assets:
            for j in i.fund_strategy_asset_weights:
                asset_weight_tickers.append(i.ticker)
                strategy_weights.append(j.strategy_weight)
                implemented_weights.append(j.implemented_weight)

        return asset_weight_tickers, implemented_weights, strategy_weights

    def select_fund_strategy_results(self, fund_name: str, strategy_name: str,
                                     business_datetime: datetime = datetime.today(),
                                     system_datetime: datetime = datetime.today()) -> Optional[Fund]:
        res = self.call_proc('arp.select_fund_strategy_results',
                             [fund_name, strategy_name, business_datetime, system_datetime])
        assets = []
        for row in res:
            fund_strategy_asset_weight = FundStrategyAssetWeight(row.strategy_weight, row.implemented_weight)
            strategy_asset_analytics = self._prep_composite_value(row.asset_analytics, StrategyAssetAnalytic)
            assets.append(Asset(row.asset_ticker, fund_strategy_asset_weights=[fund_strategy_asset_weight],
                                strategy_asset_analytics=strategy_asset_analytics))

        fund_strategy = FundStrategy(res[0]['business_datetime'], res[0]['save_output_flag'], res[0]['weight'], assets)
        fund = Fund(fund_name, res[0]['currency'], fund_strategies=[fund_strategy])

        return fund




    @staticmethod
    def _prep_composite_value(value: str, value_type: type) -> List[Any]:
        x = []
        for i in eval(value):
            y = (i[1: -1].split(','))
            y[-1] = Decimal(y[-1])

            x.append(value_type(*y))

        return x


if __name__ == '__main__':
    from datetime import datetime
    c_str = 'postgresql://d00_asset_allocation_data_migration:changeme@n00-pgsql-nexus-businessstore-writer.inv.adroot.lgim.com:54323/d00_asset_allocation_data'
    d = ArpProcCaller(c_str)

    fs = FundStrategy(datetime(2020, 1, 2), True, Decimal(1))
    s_id = 1
    u_id = 'JS89275'
    a_ws = [FundStrategyAssetWeight('a1', Decimal(1), Decimal(1)), FundStrategyAssetWeight('a2', Decimal(2), Decimal(2))]
    a_as = [
        StrategyAssetAnalytic('a1', 'performance', 'spot', Decimal(1)),
        StrategyAssetAnalytic('a1', 'signal', 'value', Decimal(2)),
        StrategyAssetAnalytic('a2', 'performance', 'spot', Decimal(3)),
        StrategyAssetAnalytic('a2', 'signal', 'value', Decimal(4))
    ]
    pcv = '0.0'
    fsr = d.insert_fund_strategy_results('f1', fs, s_id, u_id, pcv, a_ws, a_as)
    print(fsr)

