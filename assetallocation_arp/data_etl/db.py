# Import packages, classes and functions
import pandas as pd
import os
import logging
from dotenv import load_dotenv
from typing import List, Any, Dict
from sqlalchemy import create_engine

# Load .env file to get database attributes
load_dotenv()
logger = logging.getLogger('sLogger')

logger.info("db open 1")
class Db:
    procs = ['staging.load_assets']

    def __init__(self) -> None:
        """
        Db class for interacting with a database
        """
        user = os.getenv('USER')
        password = os.getenv('PASSWORD')
        host = os.getenv('HOST')
        port = os.getenv('PORT')
        database = os.getenv('DATABASE')
        self.engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')

    def call_proc(self, proc_name: str, proc_params: List[Any]) -> List[Dict[str, Any]]:
        """
        Call database stored procedure and return results.
        Raises ValueError if stored procedure is not in self.procs
        """
        if proc_name not in self.procs:
            raise ValueError(f'The stored procedure "{proc_name}" is not defined for class {self.__class__}')

        dbapi_conn = self.engine.raw_connection()

        try:
            cursor = dbapi_conn.cursor()
            cursor.callproc(proc_name, proc_params)
            column_names_list = [x[0] for x in cursor.description]
            res = cursor.fetchall()
            results = [dict(zip(column_names_list, row)) for row in res]
            cursor.close()
            dbapi_conn.commit()

        finally:
            dbapi_conn.close()

        return results

    def df_to_staging_asset(self, df: 'pd.DataFrame', **kwargs):
        """
        Write df to staging.asset
        """
        df.to_sql(name='asset', con=self.engine, schema='staging', if_exists='append', index=False, **kwargs)

        return

    def read_from_db(self):

        df = pd.read_sql_table(table_name='asset',
                               schema='staging',
                               columns=["ticker",
                                        "description",
                                        "value",
                                        "business_datetime"],
                               con=self.engine)

        # Convert date column to python datetime
        df["business_datetime"] = pd.to_datetime(df["business_datetime"], dayfirst=True)

        return df

    def get_tickers(self):

        query = """
                SELECT DISTINCT ON (ticker) ticker, description, business_datetime  
                FROM staging.asset
                ORDER BY ticker, business_datetime DESC
                """

        df = pd.read_sql(query, con=self.engine)

        # Convert date column to python datetime
        df["business_datetime"] = pd.to_datetime(df["business_datetime"], dayfirst=True)
        df["business_datetime"] = df["business_datetime"] + pd.Timedelta(days=1)
        df["business_datetime"] = df["business_datetime"].dt.strftime('%Y%m%d')

        return df
