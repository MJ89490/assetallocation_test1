# Import packages, classes and functions
import os
import logging
import logging.config
import numpy as np
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

    def bbg_data(self) -> None:
        """
        This function gets the data from Bloomberg for each instrument and is stored as a pandas data frame.
        :return: None
        """
        logger.info("Retrieving Bloomberg data")
        # Call Bloomberg class
        # Create empty list to append multiple data frames to
        # Loop through each security and respective fields to get data as a data frame
        bbg = bloomberg_data.Bloomberg()
        df_list = []
        yday_date = (datetime.today() - timedelta(days=1)).strftime("%Y%m%d")
        for index, row in self.df.iterrows():
            self.df_iteration = bbg.historicalRequest(securities=row["ticker"],
                                                      fields="PX_LAST",
                                                      startdate=row["business_datetime"],
                                                      enddate=yday_date)

            # Append data frame to df list
            df_list.append(self.df_iteration)
            logger.info(f"Loop {index + 1}/{len(self.df.index)} complete - \"{row['ticker']}\" imported")

        # Concat df list into single, large data frame
        self.df_bbg = pd.concat(df_list, axis=0, ignore_index=True)
        logger.info(f"Retrieved Bloomberg data for {len(self.df.index)} instruments")

        return

    def clean_data(self) -> pd.DataFrame:
        """
        This function cleans the Bloomberg data and outputs this as a pandas data frame.
        :return: None
        """
        logger.info("Cleaning Bloomberg data")
        # Rename column headers to match table in database
        del self.df_bbg["status"]
        col_dict = {"bbergsymbol": "ticker",
                    "bbergfield": "analytic_category",
                    "bbergdate": "business_datetime",
                    "bbergvalue": "value"}
        self.df_bbg.columns = [col_dict.get(x, x) for x in self.df_bbg.columns]

        try:
            # Convert columns to respective format types and fill in relevant columns needed for database
            self.df_bbg["ticker"] = self.df_bbg["ticker"].astype(str)
            self.df_bbg["source"] = "Bloomberg"
            self.df_bbg["value"] = self.df_bbg["value"].astype(float)
            self.df_bbg["value"] = self.df_bbg["value"].fillna(-9999)
            self.df_bbg["business_datetime"] = pd.to_datetime(self.df_bbg["business_datetime"])
            self.df_bbg["business_datetime"] = self.df_bbg["business_datetime"].fillna(datetime(1900, 1, 1))
            logger.info("Columns converted to respective data types")

            df_null_val = self.df_bbg[self.df_bbg['value'] == -9999]
            df_null_date = self.df_bbg[self.df_bbg['business_datetime'] == datetime(1900, 1, 1)]
            logging.info(f"There are {len(df_null_val.index)} null value rows:"
                         f"{df_null_val}"
                         f"")
            logging.info(f"There are {len(df_null_date.index)} null date rows:"
                         f"{df_null_date}"
                         f"")

            return self.df_bbg
        except ValueError:
            logging.info("Invalid data type inside Bloomberg data")

    def data_validation(self) -> None:
        """
        This function validates the data for the data taken from Bloomberg and performs statistical analysis to find
        outliers and possible incorrect values.
        :return: None
        """
        logging.info("Data validation started")
        # Create .xlsx file to output to
        xl_writer = pd.ExcelWriter("data_validation.xlsx", engine="xlsxwriter", options={'remove_timezone': True})

        # Sort data frame by ticker
        self.df = self.df.sort_values(by=['ticker', 'business_datetime'], ascending=[False, True])

        # Filter for dates that are not consecutive, for each instrument
        # df_date_diff = self.df.copy()
        df_date_diff = self.df.assign(date_check=self.df.business_datetime.groupby(self.df.ticker).diff())
        df_date_diff = df_date_diff[(df_date_diff["date_check"] != timedelta(days=1))]
        df_date_diff.to_excel(xl_writer, sheet_name="inconsistent_dates")

        # Filter for values that are -9999 i.e. null
        df_value_zero_null = self.df.copy()
        df_value_zero_null = df_value_zero_null[df_value_zero_null["value"] == -9999]
        df_value_zero_null.to_excel(xl_writer, sheet_name="zero_or_null_prices")

        # Filter for values that are more than 2 standard deviations from the mean
        df_value_outliers = self.df.copy()
        df_value_outliers["value_mean"] = df_value_outliers.groupby("ticker").value.transform('mean')
        df_value_outliers["value_standard_deviation"] = df_value_outliers.groupby("ticker").value.transform('std')
        df_value_outliers["value_z_score"] = (df_value_outliers["value"] - df_value_outliers["value_mean"]) / \
            df_value_outliers["value_standard_deviation"]
        df_value_outliers = df_value_outliers[df_value_outliers["value_z_score"] > 2]
        df_value_outliers.to_excel(xl_writer, sheet_name="daily_value_outliers")

        # Filter for returns (log value) that are more than 2 standard deviations from the mean
        df_return_outliers = self.df.copy()
        df_return_outliers = df_return_outliers.assign(log_return=np.log(df_return_outliers.value).groupby(
            df_return_outliers.ticker).diff())
        df_return_outliers["log_return_mean"] = df_return_outliers.groupby("ticker").log_return.transform('mean')
        df_return_outliers["log_return_standard_deviation"] = df_return_outliers.groupby("ticker")\
            .log_return.transform('std')
        df_return_outliers["log_return_z_score"] = (df_return_outliers["log_return"]
                                                    - df_return_outliers["log_return_mean"]) / df_return_outliers[
            "log_return_standard_deviation"]
        df_return_outliers = df_return_outliers[df_return_outliers["log_return_z_score"] > 2]
        df_return_outliers.to_excel(xl_writer, sheet_name="daily_log_return_outliers")

        xl_writer.save()

        logging.info("Data validation complete")

        return
