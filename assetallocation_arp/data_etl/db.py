# Import packages, classes and functions
import os
import logging
import logging.config
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from typing import List, Any, Dict, Tuple
from sqlalchemy import create_engine
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
        Data base class to connect to the Asset Allocation postgreSQL database.
        :return:
        """
        # Get database credentials from .ini file
        user = os.getenv("USER")
        password = os.getenv("PASSWORD")
        host = os.getenv("HOST")
        port = os.getenv("PORT")
        database = os.getenv("DATABASE")

        # Create database engine
        self.engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")
        logging.info(f"Database engine defined for: {database}")

    def call_proc(self, proc_name: str, proc_params: List[Any]) -> List[Dict[str, Any]]:
        """
        This functions calls database stored procedure and returns the results.
        :param proc_name: Stored procedure name, string
        :param proc_params: Stored procedure parameters, list
        :return: Results as list of dictionaries
        """
        logging.info(f"Getting stored procedure: {proc_name}")

        if proc_name not in self.procs:
            raise ValueError(f"The stored procedure '{proc_name}' is not defined for class {self.__class__}")

        dbapi_conn = self.engine.raw_connection()
        logging.info("Writing to Asset Analytic main table")
        logging.info(f"Database connection opened")
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
            logging.info(f"Database connection closed")
        logging.info(f"Writing complete for Asset Analytic main table")

        return results

    def df_to_staging_asset_analytic(self, df: pd.DataFrame) -> None:
        """
        This function writes a pandas data frame to the main asset analytic table.
        :param: Input pandas data frame
        :return:
        """
        try:
            logging.info("Writing to Asset Analytic staging table")
            # Write pandas data frame to SQL table - this is done in chunks of 10,000
            df.to_sql(name="asset_analytic", con=self.engine, schema="staging", if_exists="append", index=False,
                      method='multi', chunksize=10000)
            logging.info("Writing complete for Asset Analytic staging table")

            return
        except SQLAlchemyError as e:
            logger.info(e)

    def get_analytic(self) -> Tuple[pd.DataFrame, List[str]]:
        """
        This function gets asset analytic data from the asset analytic table. Relevant columns are
        converted to pandas datetime.
        :return: Pandas data frame of asset analytics, unique list of tickers
        """
        query = """
                SELECT ticker, description, value, business_datetime
                FROM asset.asset_analytic
                LEFT JOIN asset.asset
                ON asset_analytic.asset_id = asset.id
                WHERE upper(system_tstzrange) = 'infinity';
                """
        try:
            chunk_list = []
            i = 0
            logger.info("Reading main Asset Analytic table")
            for chunk in pd.read_sql(query, con=self.engine, chunksize=100000):
                chunk_list.append(chunk)
                i += 1
                logging.info(f"Chunk: {i} complete")
            df = pd.concat(chunk_list, ignore_index=True)
            logger.info("Reading complete for main Asset Analytic table")

            # Convert date column to python datetime
            df["business_datetime"] = pd.to_datetime(df["business_datetime"], dayfirst=True)

            # If data frame is empty, default output to be a "null" data frame which can be shown in Bokeh
            if df.empty:
                df = pd.DataFrame({"ticker": ["N/A", "N/A"],
                                   "value": [0, 0],
                                   "business_datetime": [datetime.today().strftime("%Y/%m/%d"),
                                                         datetime.today().strftime("%Y/%m/%d")],
                                   "description": ["N/A", "N/A"]})
                logger.info("No data retrieved from database - initial graph defaulted to null")

            instrument_list = df["ticker"].unique().tolist()

            return df, instrument_list
        except SQLAlchemyError as e:
            logger.info(e)

    def get_tickers(self) -> pd.DataFrame:
        """
        This function retrieves the latest tickets table as a pandas data frame and respective list.
        :return: Tickers with latest price as pandas data frame and list
        """
        logger.info("Reading tickers from database")

        # Define postgreSQL query to get table of tickers with the latest price
        # Read table as pandas data frame
        query = """
                SELECT DISTINCT ON (ticker) ticker, description, business_datetime
                FROM asset.asset AS a
                LEFT JOIN (SELECT asset_id, max(business_datetime) AS business_datetime FROM asset.asset_analytic
                 GROUP BY asset_id) as aa 
                ON a.id = aa.asset_id;
                """
        try:
            logger.info("Reading main Asset table")
            # Read given table from database as data frame
            df = pd.read_sql(query, con=self.engine, chunksize=10000)
            logger.info("Reading complete for main Asset table")

            # Convert date column to python datetime
            # Add 1 day to date column
            df["business_datetime"] = pd.to_datetime(df["business_datetime"], dayfirst=True)
            df["business_datetime"] = df["business_datetime"] + pd.Timedelta(days=1)
            # Convert to YYMMDD string datetime format
            # If instruments are futures, then datetime is set to earliest possible date to refresh time series
            df["business_datetime"] = df["business_datetime"].dt.strftime("%Y%m%d")
            df['business_datetime'].loc[df['description'].str.contains(r'(?i)\bfuture\b')]\
                = datetime(1900, 1, 1).strftime("%Y%m%d")

            return df
        except SQLAlchemyError as e:
            logger.info(e)
