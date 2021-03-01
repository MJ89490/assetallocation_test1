# Import packages, classes and functions
import os
import logging
import logging.config
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from typing import List, Any, Dict
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Load .env file to get database attributes
load_dotenv()

# Get logging config from .ini file
logging.config.fileConfig(f"{os.path.dirname(os.path.abspath(__file__))}/logging.ini", disable_existing_loggers=False)
logger = logging.getLogger("sLogger")


class Db:
    procs = ["staging.load_assets", "staging.load_asset_analytics"]

    def __init__(self) -> None:
        """
        Db class for interacting with a database
        """
        user = os.getenv("USER")
        password = os.getenv("PASSWORD")
        host = os.getenv("HOST")
        port = os.getenv("PORT")
        database = os.getenv("DATABASE")
        self.engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")

    def call_proc(self, proc_name: str, proc_params: List[Any]) -> List[Dict[str, Any]]:
        """
        Call database stored procedure and return results.
        Raises ValueError if stored procedure is not in self.procs
        """
        if proc_name not in self.procs:
            raise ValueError(f"The stored procedure '{proc_name}' is not defined for class {self.__class__}")

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

    def df_to_staging_asset(self, df: "pd.DataFrame", **kwargs):
        """
        Write data frame to asset staging table.
        :return:
        """
        logging.info("Writing data frame to Asset staging table")
        # Write pandas data frame to SQL table
        try:
            df.to_sql(name="asset", con=self.engine, schema="staging", if_exists="append", index=False, **kwargs)
            logging.info("Data frame written to Asset staging table")
            return
        except SQLAlchemyError as e:
            logger.info(e)

    def df_to_staging_asset_analytic(self, df: "pd.DataFrame", **kwargs):
        """
        Write data frame to asset analytic staging table.
        :return:
        """
        logging.info("Writing data frame to Asset Analytic staging table")
        # Write pandas data frame to SQL table
        try:
            df.to_sql(name="asset_analytic", con=self.engine, schema="staging", if_exists="append", index=False,
                      **kwargs)
            logging.info("Data frame written to Asset Analytic table")
            return
        except SQLAlchemyError as e:
            logger.info(e)

    def read_from_db(self):
        """
        This function reads a given table from the postgres database as a pandas data frame. Relevant columns are
        converted to pandas datetime.
        :return: table as pandas data frame
        """
        logger.info("Reading table from database")

        query = """
                SELECT ticker, description, value, business_datetime
                FROM asset.asset_analytic
                LEFT JOIN asset.asset
                ON asset_analytic.asset_id = asset.id
                """
        try:
            # Read given table from database as data frame
            df = pd.read_sql(query, con=self.engine)

            # Convert date column to python datetime
            df["business_datetime"] = pd.to_datetime(df["business_datetime"], dayfirst=True)
            logger.info("Reading from data base complete")

            return df

        except SQLAlchemyError as e:
            logger.info(e)

    def get_tickers(self):
        """
        This function retrieves the latest tickets table as a pandas data frame.
        :return: tickers with latest price as pandas data frame and also list
        """
        logger.info("Reading tickers with latest price from database")

        # Define postgreSQL query to get table of tickers with the latest price
        # Read table as pandas data frame
        query = """
                SELECT DISTINCT ON (ticker) ticker, description, business_datetime  
                FROM asset.asset
                LEFT JOIN asset.asset_analytic
                ON asset.id = asset_analytic.id
                ORDER BY ticker, business_datetime DESC
                """
        try:
            df = pd.read_sql(query, con=self.engine)

            # Convert date column to python datetime
            # Add 1 day to date column
            df["business_datetime"].fillna(datetime(1900, 1, 1).strftime("%Y%m%d"), inplace=True)
            df["business_datetime"] = pd.to_datetime(df["business_datetime"], dayfirst=True)
            df["business_datetime"] = df["business_datetime"] + pd.Timedelta(days=1)
            df["business_datetime"] = df["business_datetime"].dt.strftime("%Y%m%d")

            # Get existing tickers from database as list
            ticker_list = df["ticker"].tolist()

            logger.info("Table of tickers imported")

            return df, ticker_list

        except SQLAlchemyError as e:
            logger.info(e)
