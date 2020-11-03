from typing import Union, List
import datetime as dt

from assetallocation_arp.data_etl.dal.arp_proc_caller import StrategyProcCallerFactory, ArpProcCaller
from assetallocation_arp.data_etl.dal.data_models.strategy import Strategy
from assetallocation_arp.data_etl.dal.data_models.fund_strategy import FundStrategy
from assetallocation_arp.common_libraries.dal_enums.strategy import Name


def run_strategy(
        fund_name: str, strategy_weight: float, strategy: Strategy, user_id: str,
        business_datetime: dt.datetime = dt.datetime.today() - dt.timedelta(365)
) -> FundStrategy:
    pc = StrategyProcCallerFactory().get_proc_caller(strategy.name)()
    strategy_version = pc.insert_strategy(strategy, user_id)
    strategy = pc.select_strategy_with_asset_analytics(strategy_version, business_datetime)
    fs = FundStrategy(fund_name, strategy.name, strategy_version, strategy_weight)
    fs.analytics, fs.asset_weights = strategy.run()
    pc.insert_fund_strategy_results(fs, user_id)
    return fs


def get_strategy_versions(strategy_name: Union[str, Name]) -> List[int]:
    apc = ArpProcCaller()
    return apc.select_strategy_versions(strategy_name)
