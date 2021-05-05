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
    def __init__(self, non_futures_list, futures_list, non_futures_start_date, futures_start_date):
        """
        This class extracts ticker data from Bloomberg, transforms this to valid data types and uploads to the
        postgreSQL database.
        :param non_futures_list: list of non-futures instruments
        :param futures_list: df includes
        :param non_futures_start_date: start date for futures instruments, strftime
        :param futures_start_date: non_futures_start_date: start date for non-futures instruments, strftime
        """
        self.non_futures_list = non_futures_list
        self.futures_list = futures_list
        self.non_futures_start_date = non_futures_start_date
        self.futures_start_date = futures_start_date

        self.df_bbg_non_future = pd.DataFrame()
        self.df_bbg_future = pd.DataFrame()
        self.df_bbg = pd.DataFrame()

    def bbg_data(self) -> None:
        """
        This function gets the data from Bloomberg for each instrument and is stored as a pandas data frame.
        :return:
        """
        logger.info("Retrieving Bloomberg data")
        # Loop through each security and respective fields to get data as a data frame
        yday_date = (datetime.today() - timedelta(days=1)).strftime("%Y%m%d")

        # call Bloomberg API and get data for all instruments
        # combine non-futures and futures data frames
        bbg = bloomberg_data.Bloomberg()
        self.df_bbg_non_future = bbg.historicalRequest(securities=self.non_futures_list,
                                                       fields="PX_LAST",
                                                       startdate=self.non_futures_start_date,
                                                       enddate=yday_date)

        self.df_bbg_future = bbg.historicalRequest(securities=self.futures_list,
                                                   fields="PX_LAST",
                                                   startdate=self.futures_start_date,
                                                   enddate=yday_date)

        self.df_bbg = self.df_bbg_non_future.append(self.df_bbg_future)

        # filter data frame for errors and non-errors
        df_bbg_error = self.df_bbg[~self.df_bbg["status"].str.contains("DONE")]
        error_tickers = df_bbg_error["bbergsymbol"].unique()
        logger.info(f"{len(error_tickers)} tickers not retrieved: {error_tickers}")

        self.df_bbg = self.df_bbg[self.df_bbg["status"].str.contains("DONE")]
        logger.info(f"{len(self.df_bbg.index)} rows retrieved from Bloomberg")

        return

    def clean_data(self) -> pd.DataFrame:
        """
        This function cleans the Bloomberg data and outputs this as a pandas data frame.
        :return:
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
            self.df_bbg["business_datetime"] = pd.to_datetime(self.df_bbg["business_datetime"])
            logger.info("Columns converted to respective data types")

            return self.df_bbg
        except ValueError:
            logging.info("Invalid data type inside Bloomberg data")


def data_validation(df: pd.DataFrame) -> None:
    """
    This function validates the data for the data taken from Bloomberg and performs statistical analysis to find
    outliers and possible incorrect values.
    :param df: Pandas data frame of data to validate
    :return:
    """
    logging.info("Data validation started")
    # Create .xlsx file to output to
    xl_writer = pd.ExcelWriter("data_validation.xlsx", engine="xlsxwriter", options={'remove_timezone': True})

    # Sort data frame by ticker
    df = df.sort_values(by=['ticker', 'business_datetime'], ascending=[False, True])

    # Filter for dates that are not consecutive, for each instrument
    # df_date_diff = df.copy()
    df_date_diff = df.assign(date_check=df.business_datetime.groupby(df.ticker).diff())
    df_date_diff = df_date_diff[(df_date_diff["date_check"] != timedelta(days=1))]
    df_date_diff.to_excel(xl_writer, sheet_name="inconsistent_dates")

    # Filter for values that are null
    df_value_zero_null = df.copy()
    df_value_zero_null = df_value_zero_null[(df_value_zero_null["value"].isna()) |
                                            (df_value_zero_null["value"] == 0)]
    df_value_zero_null.to_excel(xl_writer, sheet_name="zero_or_null_prices")

    # Filter for values that are more than 2 standard deviations from the mean
    df_value_outliers = df.copy()
    df_value_outliers["value_mean"] = df_value_outliers.groupby("ticker").value.transform('mean')
    df_value_outliers["value_standard_deviation"] = df_value_outliers.groupby("ticker").value.transform('std')
    df_value_outliers["value_z_score"] = (df_value_outliers["value"] - df_value_outliers["value_mean"]) / \
                                         df_value_outliers["value_standard_deviation"]
    df_value_outliers = df_value_outliers[df_value_outliers["value_z_score"] > 2]
    df_value_outliers.to_excel(xl_writer, sheet_name="daily_value_outliers")

    # Filter for returns (log value) that are more than 2 standard deviations from the mean
    df_return_outliers = df.copy()
    df_return_outliers = df_return_outliers.assign(log_return=np.log(df_return_outliers.value).groupby(
        df_return_outliers.ticker).diff())
    df_return_outliers["log_return_mean"] = df_return_outliers.groupby("ticker").log_return.transform('mean')
    df_return_outliers["log_return_standard_deviation"] = df_return_outliers.groupby("ticker") \
        .log_return.transform('std')
    df_return_outliers["log_return_z_score"] = (df_return_outliers["log_return"]
                                                - df_return_outliers["log_return_mean"]) / df_return_outliers[
                                                   "log_return_standard_deviation"]
    df_return_outliers = df_return_outliers[df_return_outliers["log_return_z_score"] > 2]
    df_return_outliers.to_excel(xl_writer, sheet_name="daily_log_return_outliers")

    xl_writer.save()

    logging.info("Data validation complete")

    return
