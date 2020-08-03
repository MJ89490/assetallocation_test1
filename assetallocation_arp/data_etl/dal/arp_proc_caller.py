from typing import List, Tuple
from decimal import Decimal

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

        def prep_aa(r: str) -> List[AssetAnalytic]:
            aa = []

            for i in eval(r):
                a = (i[1: -1].split(','))
                a[-1] = Decimal(a[-1])

                aa.append(AssetAnalytic(*a))

            return aa

        return [(prep_aa(r.pop('asset_analytic')), Asset(**r)) for r in assets]

    def insert_fund_strategy_results(self, fund_name: str, fund_strategy: FundStrategy, strategy_id: int, user_id: str,
                                     python_code_version: str, asset_weights: List[FundStrategyAssetWeight],
                                     asset_analytics: List[StrategyAssetAnalytic]) -> bool:
        asset_weight_tickers, implemented_weights, strategy_weights = self._split_asset_weights(asset_weights)
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
    def _split_asset_analytics(asset_analytics):
        asset_analytic_tickers, analytic_types, analytic_subtypes, analytic_values = [], [], [], []
        for i in asset_analytics:
            asset_analytic_tickers.append(i.asset_ticker)
            analytic_types.append(i.analytic_type)
            analytic_subtypes.append(i.analytic_subtype)
            analytic_values.append(i.value)

        return asset_analytic_tickers, analytic_types, analytic_subtypes, analytic_values

    @staticmethod
    def _split_asset_weights(asset_weights):
        asset_weight_tickers, strategy_weights, implemented_weights = [], [], []
        for i in asset_weights:
            asset_weight_tickers.append(i.asset_ticker)
            strategy_weights.append(i.strategy_weight)
            implemented_weights.append(i.implemented_weight)
        return asset_weight_tickers, implemented_weights, strategy_weights


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

