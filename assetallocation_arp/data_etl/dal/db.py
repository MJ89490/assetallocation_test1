from typing import List, Any, Dict

from sqlalchemy import create_engine


class Db:
    procs = []

    def __init__(self, conn_str: str) -> None:
        """Db class for interacting with a database"""
        self.engine = create_engine(conn_str)

    def call_proc(self, proc_name: str, proc_params: List[Any]) -> List[Dict[str, Any]]:
        """Call database stored procedure and return results.
        Raises ValueError if stored procedure is not in self.procs
        """
        if proc_name not in self.procs:
            raise ValueError(f'The stored procedure "{proc_name}" is not defined for class {self.__class__}')

        dbapi_conn = self.engine.raw_connection()

        try:
            cursor = dbapi_conn.cursor()
            cursor.itersize = 100
            cursor.callproc(proc_name, proc_params)
            column_names_list = [x[0] for x in cursor.description]
            res = cursor.fetchall()
            results = [dict(zip(column_names_list, row)) for row in res]
            cursor.close()
            dbapi_conn.commit()

        finally:
            dbapi_conn.close()

        return results
