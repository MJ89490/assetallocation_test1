from typing import List, Any, Dict
from os import environ
from json import loads

from sqlalchemy import create_engine


class Db:
    procs = ['staging.load_assets']

    def __init__(self) -> None:
        """Db class for interacting with a database"""
        config = loads(environ.get('DATABASE', '{}'))
        user = config.get('USER')
        password = config.get('PASSWORD')
        host = config.get('HOST')
        port = config.get('PORT')
        database = config.get('DATABASE')
        self.engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')

    def call_proc(self, proc_name: str, proc_params: List[Any]) -> List[Dict[str, Any]]:
        """Call database stored procedure and return results.
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
        """Write df to staging.asset"""
        df.to_sql(name='asset', con=self.engine, schema='staging', if_exists='append', index=False, **kwargs)


if __name__ == '__main__':
    import pandas as pd

    df = pd.DataFrame([['HSI Index', 'asset name', 'some description', 'Equity', 'US Equities', 'USD', 'AUD', True, 'd', 'Bloomberg', 1.5, '2020-01-02']],
                      columns=['ticker', 'name', 'description', 'asset_category', 'asset_subcategory', 'currency',
                               'country', 'is_tr', 'analytic_category', 'source', 'value', 'business_datetime'])

    # loads the dataframe into staging.asset
    d = Db()
    d.df_to_staging_asset(df)

    # staging.load_assets proc is not yet implemented. Once finished it will copy the data from staging.asset
    # to asset.asset, asset.asset_group and asset.asset_analytics
    d.call_proc('staging.load_assets', [])

    # see data for testing purposes. avoid calling engine.execute() with raw sql in production code
    selected = d.engine.execute('SELECT * FROM staging.asset')
    for i in selected:
        print(i)

    # empty staging.asset table for testing purposes. avoid calling engine.execute() with raw sql in production code

    d.engine.execute('DELETE FROM staging.asset')
