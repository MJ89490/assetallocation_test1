from typing import Union, List
import datetime as dt

from assetallocation_arp.arp_strategies import run_times, run_effect, run_fica
from assetallocation_arp.data_etl.dal.arp_proc_caller import TimesProcCaller, EffectProcCaller, ArpProcCaller, FicaProcCaller
from assetallocation_arp.data_etl.dal.data_models.strategy import Strategy, Times, Effect, Fica
from assetallocation_arp.data_etl.dal.data_models.fund_strategy import FundStrategy
from assetallocation_arp.common_libraries.dal_enums.strategy import Name


def run_strategy(fund_name: str, strategy_weight: float, strategy: Strategy, user_id: str,
                 business_datetime: dt.datetime = dt.datetime.today() - dt.timedelta(365)) -> FundStrategy:
    if isinstance(strategy, Times):
        pc = TimesProcCaller()
        times_version = pc.insert_times(strategy, user_id)
        strategy.asset_inputs = pc.select_times_assets_with_analytics(times_version, business_datetime)
        fs = FundStrategy(fund_name, Name.times, times_version, strategy_weight)
        fs.analytics, fs.asset_weights = run_times(strategy)

    elif isinstance(strategy, Effect):
        pc = EffectProcCaller()
        effect_version = pc.insert_effect(strategy, user_id)
        strategy.asset_inputs = pc.select_effect_assets_with_analytics(effect_version, business_datetime)

        fs = FundStrategy(fund_name, Name.effect, effect_version, strategy_weight)
        fs.analytics, fs.asset_weights = run_effect(strategy)

    elif isinstance(strategy, Fica):
        pc = FicaProcCaller()
        fica_version = pc.insert_fica(strategy, user_id)
        strategy.grouped_asset_inputs = pc.select_fica_assets_with_analytics(fica_version)

        fs = FundStrategy(fund_name, Name.fica, fica_version, strategy_weight)
        fs.analytics, fs.asset_weights = run_fica(strategy)

    else:
        raise TypeError(f'strategy must be of type Strategy')

    pc.insert_fund_strategy_results(fs, user_id)

    return fs


def get_strategy_versions(strategy_name: Union[str, Name]) -> List[int]:
    apc = ArpProcCaller()
    return apc.select_strategy_versions(strategy_name)
