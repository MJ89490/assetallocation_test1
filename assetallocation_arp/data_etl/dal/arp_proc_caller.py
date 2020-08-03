from typing import List, Tuple
from decimal import Decimal

from assetallocation_arp.data_etl.dal.db import Db
from assetallocation_arp.data_etl.dal.times import Times
from assetallocation_arp.data_etl.dal.asset import Asset
from assetallocation_arp.data_etl.dal.asset_analytic import AssetAnalytic


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


if __name__ == '__main__':
    c_str = 'postgresql://d00_asset_allocation_data_migration:changeme@n00-pgsql-nexus-businessstore-writer.inv.adroot.lgim.com:54323/d00_asset_allocation_data'
    d = ArpProcCaller(c_str)

    ta = d.select_times_assets(9, '2020-01-02')
    print(ta)
