from typing import List, Any, Dict
from datetime import datetime

from sqlalchemy import create_engine

from .proc import Proc
from .user import User
from .fund import Fund
from .strategy import Strategy
from .fundstrategy import FundStrategy
from .currency import Currency


class Db:
    procs = Proc.__members__.keys()

    def __init__(self, conn_str: str):
        self.engine = create_engine(conn_str)
        self.dbapi_conn = self.engine.raw_connection()

    def call_proc(self, proc_name: str, proc_params: List[Any]) -> List[Any]:
        if proc_name not in self.procs:
            raise ValueError(f'The stored procedure "{proc_name}" is not defined for the class Db')

        try:
            cursor = self.dbapi_conn.cursor()
            cursor.callproc(proc_name, proc_params)
            results = list(cursor.fetchall())
            cursor.close()
            self.dbapi_conn.commit()

        finally:
            self.dbapi_conn.close()

        return results


    def get_times_strategy_id(self, name, description, day_of_week, frequency, leverage_type, long_signals,
                              short_signals, time_lag, volatility_window) -> int:
        pass
        strategy_id = 'foo'
        return strategy_id

    def get_user_by_email(self, user_email: str) -> User:
        row = self.get_row_where_equal('user', 'user', {'email': user_email})
        return User(row.id, row.email, row.name)

    def get_row_where_equal(self, schema: str, table: str, column_values: Dict[str, Any]):
        pass

    def get_user_by_id(self, user_id: str) -> User:
        row = self.get_row_where_equal('user', 'user', {'id': user_id})
        return User(row.id, row.email, row.name)

    # TODO test the below
    def get_fund(self, name: str) -> Fund:
        fund_id, currency = self.call_proc(Proc.select_fund.name, [name])
        return Fund(name, Currency(currency))

    def get_fund_strategy(self, fund_name: str, strategy_name: str, business_datetime: datetime,
                          system_datetime: datetime) -> FundStrategy:
        """select * from fund_strategy where id = fund_strategy_id"""
        (s_user_email, s_user_id, s_user_name, s_name, description, fs_user_email, fs_user_id, fs_user_name, currency,
         f_name, save_output_flag, weight) = self.call_proc(Proc.select_fund_strategy.name,
                                                            [fund_name, strategy_name, business_datetime,
                                                             system_datetime])
        s_user = User(s_user_id, s_user_email, s_user_name)
        s = Strategy(s_name, s_user, description)
        fs_user = User(fs_user_id, fs_user_email, fs_user_name)
        f = Fund(f_name, Currency(currency))
        return FundStrategy(business_datetime, f, save_output_flag, s, weight, fs_user)
