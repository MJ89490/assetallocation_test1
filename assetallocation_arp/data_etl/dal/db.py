from typing import List, Any, Dict

from sqlalchemy import create_engine


class Db:
    def __init__(self, conn_str: str):
        self.engine = create_engine(conn_str)
        self.dbapi_conn = self.engine.raw_connection()

    def call_proc(self, proc_name, proc_params: List[Any]):
        try:
            cursor = self.dbapi_conn.cursor()
            cursor.callproc(proc_name, proc_params)
            results = list(cursor.fetchall())
            cursor.close()
            self.dbapi_conn.commit()

        finally:
            self.dbapi_conn.close()

        return results

    def get_row_where_equal(self, schema: str, table: str, column_values: Dict[str, Any]):
        pass