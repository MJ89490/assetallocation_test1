from typing import Union, List

from datetime import datetime

from assetallocation_arp.arp_strategies import run_times
from assetallocation_arp.data_etl.dal.arp_proc_caller import ArpProcCaller
from assetallocation_arp.data_etl.dal.data_models.strategy import Strategy, Times
from assetallocation_arp.data_etl.dal.data_models.fund_strategy import FundStrategy
from assetallocation_arp.common_libraries.dal_enums.strategy import Name


def run_strategy(fund_name: str, strategy_weight: float, strategy: Strategy, user_id: str,
                 business_datetime: datetime = datetime.today()) -> FundStrategy:
    if isinstance(strategy, Times):
        apc = ArpProcCaller()
        times_version = apc.insert_times(strategy, user_id)
        strategy.asset_inputs = apc.select_times_assets_with_analytics(times_version, business_datetime)

        fs = FundStrategy(fund_name, Name.times, times_version, strategy_weight)
        fsaa, fsaw = run_times(strategy)
        fs.asset_weights = fsaw
        fs.asset_analytics = fsaa

    else:
        raise TypeError(f'strategy must be of type Strategy')

    apc.insert_fund_strategy_results(fs, user_id)

    return fs


def get_strategy_versions(strategy_name: Union[str, Name]) -> List[int]:
    apc = ArpProcCaller()
    return apc.select_strategy_versions(strategy_name)
