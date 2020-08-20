from datetime import datetime
from decimal import Decimal

from assetallocation_arp.arp_strategies import run_times
from assetallocation_arp.data_etl.dal.arp_proc_caller import ArpProcCaller
from assetallocation_arp.data_etl.dal.data_models.strategy import Strategy, Times
from assetallocation_arp.data_etl.dal.data_models.fund_strategy import FundStrategy


def run_strategy(fund_name: str, strategy_weight: Decimal, strategy: Strategy, user_id: str,
                 business_datetime: datetime = datetime.today()) -> FundStrategy:
    if isinstance(strategy, Times):
        apc = ArpProcCaller()
        times_version = apc.insert_times(strategy, user_id)
        strategy.assets = apc.select_times_assets_with_analytics(times_version, business_datetime)

        fs = run_times(fund_name, strategy, strategy_weight, times_version)

        apc.insert_fund_strategy_results(fs, user_id)

    else:
        raise TypeError(f'strategy must be of type Strategy')

    return fs
