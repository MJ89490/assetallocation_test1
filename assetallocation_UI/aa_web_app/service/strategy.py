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
    """Inserts strategy object data into database. Reads asset analytics from
    database to enable running of strategy, producing outputs of
    FundStrategyAnalytics and FundStrategyAssetWeights which are written into
    the database.
    :return FundStrategy object containing outputs of strategy run
    """
    pc = StrategyProcCallerFactory.get_proc_caller(strategy.name)()
    pc.insert_strategy(strategy, user_id)
    pc.add_asset_analytics_to_strategy(strategy, business_datetime)
    fs = FundStrategy(fund_name, strategy.name, strategy.version, strategy_weight)
    fs.analytics, fs.asset_weights = strategy.run()
    pc.insert_fund_strategy_results(fs, user_id)
    return fs


def get_strategy_versions(strategy_name: Union[str, Name]) -> List[int]:
    """Get list of existing strategy versions from database"""
    apc = ArpProcCaller()
    return apc.select_strategy_versions(strategy_name)
