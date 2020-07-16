from typing import List, Any

from pandas import DataFrame

from .db import Db
from .user import User


def class_attributes_to_df(cls_instances: List[Any]) -> DataFrame:
    if not all(isinstance(i, type(cls_instances[0])) for i in cls_instances):
        raise TypeError('All cls_instances should be of the same type')

    cols = [k[1:] if k.startswith('_') else k for k in cls_instances[0].__dict__.keys()]
    return DataFrame([[v for v in cls.__dict__.values()] for cls in cls_instances], columns=cols)


# TODO test the below
def get_user_by_email(db: Db, user_email: str) -> User:
    row = db.get_row_where_equal('user', 'user', {'email': user_email})
    return User(row.email, row.id, row.name)


# TODO test the below
def get_user_by_id(db: Db, user_id: str) -> User:
    row = db.get_row_where_equal('user', 'user', {'id': user_id})
    return User(row.email, row.id, row.name)


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
