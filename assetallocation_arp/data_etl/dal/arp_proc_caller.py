from typing import List
from decimal import Decimal
from datetime import datetime

from assetallocation_arp.data_etl.dal.db import Db
from assetallocation_arp.data_etl.dal.strategy import Times
from data_etl.dal.asset_analytic import AssetAnalytic
from assetallocation_arp.data_etl.dal.fundstrategy import FundStrategy, FundStrategyAssetAnalytic, FundStrategyAssetWeight
from assetallocation_arp.data_etl.dal.type_converter import month_interval_to_int
from assetallocation_arp.data_etl.dal.asset import TimesAsset
from assetallocation_arp.common_enums.strategy import Name
from assetallocation_arp.data_etl.dal.validate import check_value


class ArpProcCaller(Db):
    def insert_times_strategy(self, times: Times, user_id, asset_tickers: List[str]) -> int:
        t_version = self.call_proc('arp.insert_times_strategy',
                                   [times.description, user_id, times.time_lag, times.leverage_type,
                                    times.volatility_window, times.short_signals, times.long_signals, times.frequency,
                                    times.day_of_week, asset_tickers])

        return t_version[0]

    def select_times_strategy(self, times_version) -> Times:
        row = self.call_proc('arp.select_times_strategy', [times_version])[0]
        t = Times(row['day_of_week'], row['frequency'], row['leverage_type'], row['long_signals'], row['short_signals'],
                  -month_interval_to_int(row['time_lag']), row['volatility_window'])
        t.version = times_version
        t.description = row['description']
        return t

    # TODO rename database column arp.asset.asset_class to arp.asset.category
    def select_times_assets(self, times_version, business_datetime) -> List[TimesAsset]:
        res = self.call_proc('arp.select_times_assets', [times_version, business_datetime])

        times_assets = []
        for r in res:
            t = TimesAsset(r['ticker'], r['category'], r['country'], r['currency'], r['name'], r['asset_type'],
                           r['s_leverage'], r['signal_ticker'], r['future_ticker'], r['cost'])
            t.description = r['description']

            # TODO find way to remove eval
            for i in eval(r['asset_analytic']):
                source, category, value = (i[1: -1].split(','))
                value = Decimal(value)

                t.add_analytic(AssetAnalytic(r['ticker'], source, category, value))

            times_assets.append(t)

        return times_assets

    # TODO investigate if composite types would be better for passing data to sql function
    def insert_fund_strategy_results(self, fund_strategy: FundStrategy, user_id: str) -> bool:
        asset_weight_tickers, implemented_weights, strategy_weights = self._split_weights(fund_strategy.asset_weights)
        asset_analytic_tickers, analytic_types, analytic_subtypes, analytic_values = self._split_analytics(fund_strategy.asset_analytics)

        fund_strategy_id = self.call_proc('arp.insert_fund_strategy_results',
                                          [fund_strategy.business_datetime, fund_strategy.fund_name,
                                           fund_strategy.output_is_saved, fund_strategy.strategy_name,
                                           fund_strategy.strategy_version, fund_strategy.weight, user_id,
                                           fund_strategy.python_code_version, asset_weight_tickers, strategy_weights,
                                           implemented_weights, asset_analytic_tickers, analytic_types,
                                           analytic_subtypes, analytic_values])[
            0]

        return fund_strategy_id is not None

    @staticmethod
    def _split_analytics(analytics: List[FundStrategyAssetAnalytic]):
        asset_tickers, categories, subcategories, values = [], [], [], []
        for i in analytics:
            asset_tickers.append(i.asset_ticker)
            categories.append(i.category)
            subcategories.append(i.subcategory)
            values.append(i.value)

        return asset_tickers, categories, subcategories, values

    @staticmethod
    def _split_weights(weights: List[FundStrategyAssetWeight]):
        asset_tickers, strategy_weights, implemented_weights = [], [], []
        for i in weights:
            asset_tickers.append(i.asset_ticker)
            strategy_weights.append(i.strategy_weight)
            implemented_weights.append(i.implemented_weight)

        return asset_tickers, implemented_weights, strategy_weights

    # TODO rename save_output_flag to output_is_saved in table arp.fund_strategy
    def select_fund_strategy_results(self, fund_name: str, strategy_name: Name,
                                     business_datetime: datetime = datetime.today(),
                                     system_datetime: datetime = datetime.today()) -> FundStrategy:
        check_value(strategy_name, Name.__members__.keys())
        res = self.call_proc('arp.select_fund_strategy_results',
                             [fund_name, strategy_name, business_datetime, system_datetime])

        fund_strategy = FundStrategy(fund_name, strategy_name, res[0]['strategy_version'], res[0]['weight'])
        fund_strategy.business_datetime = res[0]['business_datetime']
        fund_strategy.output_is_saved = res[0]['output_is_saved']
        fund_strategy.python_code_version = res[0]['python_code_version']

        for row in res:
            aw = FundStrategyAssetWeight(row['asset_ticker'], row['strategy_weight'])
            aw.implemented_weight = row['implemented_weight']
            fund_strategy.add_fund_strategy_asset_weight(aw)

            # TODO find way to remove eval
            for i in eval(row['asset_analytics']):
                category, subcategory, value = (i[1: -1].split(','))
                value = Decimal(value)
                fund_strategy.add_fund_strategy_asset_analytic(FundStrategyAssetAnalytic(row['asset_ticker'], category,
                                                                                         subcategory, value))

        return fund_strategy


if __name__ == '__main__':
    from datetime import datetime
    c_str = 'postgresql://d00_asset_allocation_data_migration:changeme@n00-pgsql-nexus-businessstore-writer.inv.adroot.lgim.com:54323/d00_asset_allocation_data'
    d = ArpProcCaller(c_str)

    # d.select_times_strategy(1)
    # ta = d.select_times_assets(1, datetime(2020, 1, 2))
    # print(ta)
    # for i in ta:
    #     for j in i.asset_analytics:
    #         print(j.asset_ticker, j.source, j.category, j.value)

    fs = d.select_fund_strategy_results('f1', 'times')

    print(fs)
    #
    # fs = FundStrategy(datetime(2020, 1, 2), True, Decimal(1))
    # s_id = 1
    # u_id = 'JS89275'
    # a_ws = [FundStrategyAssetWeight('a1', Decimal(1), Decimal(1)), FundStrategyAssetWeight('a2', Decimal(2), Decimal(2))]
    # a_as = [
    #     StrategyAssetAnalytic('a1', 'performance', 'spot', Decimal(1)),
    #     StrategyAssetAnalytic('a1', 'signal', 'value', Decimal(2)),
    #     StrategyAssetAnalytic('a2', 'performance', 'spot', Decimal(3)),
    #     StrategyAssetAnalytic('a2', 'signal', 'value', Decimal(4))
    # ]
    # pcv = '0.0'
    # fsr = d.insert_fund_strategy_results('f1', fs, s_id, u_id, pcv, a_ws, a_as)
    # print(fsr)

