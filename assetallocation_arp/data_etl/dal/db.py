from typing import List, Any, Dict

from sqlalchemy import create_engine

from assetallocation_arp.data_etl.dal.proc import Proc


class Db:
    procs = Proc.__members__.keys()

    def __init__(self, conn_str: str):
        self.engine = create_engine(conn_str)

    def call_proc(self, proc_name: str, proc_params: List[Any]) -> List[Any]:
        if proc_name not in self.procs:
            raise ValueError(f'The stored procedure "{proc_name}" is not defined for the class Db')

        dbapi_conn = self.engine.raw_connection()

        try:
            cursor = dbapi_conn.cursor()
            cursor.callproc(proc_name, proc_params)
            column_names_list = [x[0] for x in cursor.description]
            results = [dict(zip(column_names_list, row)) for row in cursor.fetchall()]
            cursor.close()
            dbapi_conn.commit()

        finally:
            dbapi_conn.close()

        return results
