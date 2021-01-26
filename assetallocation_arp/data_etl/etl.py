# Import packages, classes and functions
import os
import logging
import logging.config
import pandas as pd
from datetime import datetime, timedelta
import bloomberg_data
from db import Db

# Get logging config from .ini file
logging.config.fileConfig(f"{os.path.dirname(os.path.abspath(__file__))}/logging.ini", disable_existing_loggers=False)
logger = logging.getLogger("sLogger")


class ETLProcess:
    def __init__(self, df):
        self.df = df
        self.df_iteration = pd.DataFrame()
        self.df_bbg = pd.DataFrame()

    def clean_input(self):
        """
        This function cleans the input data from the user uploaded .csv file.
        :return: Clean table of uploaded .csv as pandas data frame
        """
        logger.info("Cleaning user uploaded .csv file")

        # Get list of existing tickers from the database
        db = Db()
        _, tickers_in_db = db.get_tickers()
        # Filter data frame to not include instruments already in the data frame
        self.df = self.df[~self.df["ticker"].isin(tickers_in_db)].reset_index()

        try:
            # Convert columns to respective format types
            self.df["ticker"] = self.df["ticker"].astype(str)
            self.df["name"] = self.df["name"].astype(str)
            self.df["description"] = self.df["description"].astype(str)
            self.df["asset_category"] = self.df["asset_category"].astype(str)
            self.df["asset_subcategory"] = self.df["asset_subcategory"].astype(str)
            self.df["currency"] = self.df["currency"].astype(str)
            self.df["country"] = self.df["country"].astype(str)
            self.df["is_tr"] = self.df["is_tr"].astype(str)
            self.df["analytic_category"] = self.df["analytic_category"].astype(str)
            self.df["business_datetime"] = datetime(1900, 1, 1).strftime("%Y%m%d")
        except ValueError:
            logging.info("Invalid data type inside input data")

        logger.info("Cleaning of input table complete")

        return self.df

    def bbg_data(self):
        """
        This function gets the data from Bloomberg for each instrument and is stored as a pandas data frame.
        :return: Table of Bloomberg data as pandas data frame
        """
        logger.info("Retrieving Bloomberg data")

        # Call Bloomberg class
        # Create empty list to append multiple data frames to
        # Loop through each security and respective fields to get data as a data frame
        bbg = bloomberg_data.Bloomberg()
        df_list = []
        for index, row in self.df.iterrows():
            self.df_iteration = bbg.historicalRequest(securities=row["ticker"],
                                                      fields=row["description"],
                                                      startdate=row["business_datetime"],
                                                      enddate=(datetime.today() - timedelta(days=1)).strftime("%Y%m%d"))

            # Append data frame to df list
            df_list.append(self.df_iteration)

            logger.info(f"Loop {index +  1}/{len(self.df.index)} complete - \"{row['ticker']}\" imported")

        # Concat df list into single, large data frame
        self.df_bbg = pd.concat(df_list, axis=0, ignore_index=True)

        logger.info("Bloomberg data collected and stored as data frame")

        return self.df_bbg

    def clean_data(self):
        """
        This function cleans the Bloomberg data and outputs this as a pandas data frame.
        :return: Table of cleaned Bloomberg data as pandas data frame
        """
        logger.info("Cleaning Bloomberg data")

        # Rename column headers to match table in database
        col_dict = {"bbergsymbol": "ticker",
                    "bbergfield": "description",
                    "bbergdate": "business_datetime",
                    "bbergvalue": "value",
                    "status": "source"}
        self.df_bbg.columns = [col_dict.get(x, x) for x in self.df_bbg.columns]

        try:
            # Convert columns to respective format types and fill in relevant columns needed for database
            self.df_bbg["ticker"] = self.df_bbg["ticker"].astype(str)
            self.df_bbg["name"] = "TEST"#self.df_input["name"]
            self.df_bbg["description"] = self.df_bbg["description"].astype(str)
            self.df_bbg["asset_category"] = "TEST"# self.df_input["asset_category"]
            self.df_bbg["asset_subcategory"] = "TEST"# self.df_input["asset_subcategory"]
            self.df_bbg["currency"] = "TEST"# self.df_input["currency"]
            self.df_bbg["country"] = "TEST"# self.df_input["country"]
            self.df_bbg["is_tr"] = "TRUE"# self.df_input["is_tr"]
            self.df_bbg["analytic_category"] = "TEST"# self.df_input["analytic_category"]
            self.df_bbg["source"] = self.df_bbg["source"].astype(str)
            self.df_bbg["value"] = self.df_bbg["value"].astype(float)
            self.df_bbg["business_datetime"] = pd.to_datetime(self.df_bbg["business_datetime"])
            logger.info("Columns converted to respective data types")

            return self.df_bbg
        except ValueError:
            logging.info("Invalid data type inside Bloomberg data")

    def upload_data(self):
        """
        This function uploads the cleaned Bloomberg data to the postgreSQL database.
        :return:
        """
        logger.info("Writing data to database")

        # Call function that uploads data frame to SQL database from respective class
        db = Db()
        db.df_to_staging_asset(self.df_bbg)
        logger.info("Data written to database")

        return
