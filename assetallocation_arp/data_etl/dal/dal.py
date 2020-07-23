from typing import List, Any, Optional
from datetime import datetime

from pandas import DataFrame

from .user import User
from .times import Times
from .fund import Fund
from .currency import Currency
from .fundstrategy import FundStrategy
from assetallocation_arp.common_libraries.day_of_week import DayOfWeek
from .db import Db


def class_attributes_to_df(cls_instances: List[Any]) -> DataFrame:
    if not all(isinstance(i, type(cls_instances[0])) for i in cls_instances):
        raise TypeError('All cls_instances should be of the same type')

    cols = [k[1:] if k.startswith('_') else k for k in cls_instances[0].__dict__.keys()]
    return DataFrame([[v for v in cls.__dict__.values()] for cls in cls_instances], columns=cols)


def get_fund_strategy_asset_analytics(fund_name, strategy_name, business_datetime, system_datetime):
    """"""
    pass


def get_fund_strategy_asset_weights(fund_name, strategy_name, business_datetime, system_datetime):
    pass


def get_fund_strategies(fund_name, business_datetime, system_datetime):
    pass


# TODO find out where fund name + currency comes from
def insert_times_fund_strategy(week_day: str, frequency: str, leverage_type: str, long_signals: List[float],
                               short_signals: List[float], time_lag: int, volatility_window: int,
                               strategy_weight: float, user_id, save_output_flag: bool, fund_name, fund_currency,
                               new_strategy: bool, business_datetime: datetime = datetime.today(),
                               asset_tickers: Optional[List[str]] = None) -> int:
    """Save inputs to times strategy in database"""
    conn_str = 'foo'  # TODO set configuration files
    db = Db(conn_str)

    times = Times(User(user_id), DayOfWeek[week_day].value, frequency, leverage_type, long_signals, short_signals,
                  time_lag, volatility_window)

    f = Fund(fund_name, Currency(fund_currency))
    fs = FundStrategy(business_datetime, f, save_output_flag, times, strategy_weight, User(user_id))

    strategy_id = fs.strategy.insert(db, asset_tickers) if new_strategy else fs.strategy.get_id()
    fund_strategy_id = fs.insert(db, strategy_id)

    return fund_strategy_id
