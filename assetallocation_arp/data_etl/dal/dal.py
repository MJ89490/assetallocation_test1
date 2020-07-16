from typing import List, Any

import pandas as pd


def class_attributes_to_df(cls_instances: List[Any]):
    cols = [k[1:] if k.startswith('_') else k for k in cls_instances[0].__dict__.keys()]
    return pd.DataFrame([[v for v in cls.__dict__.values()] for cls in cls_instances], columns=cols)


def add_fund_strategy():
    """add a new fund_strategy"""
    pass


def get_fund_strategy(fund_name, strategy_name, business_datetime, system_datetime):
    """select * from fund_strategy where id = fund_strategy_id"""
    pass


def get_fund_strategy_asset_analytics(fund_name, strategy_name, business_datetime, system_datetime):
    """"""
    pass


def get_fund_strategy_asset_weights(fund_name, strategy_name, business_datetime, system_datetime):
    pass


def get_fund_strategies(fund_name, business_datetime, system_datetime):
    pass
