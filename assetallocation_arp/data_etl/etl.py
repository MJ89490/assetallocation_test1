# TODO: timeit, data type checking, log file
# TODO: DB: frequency of data updating then uploading; data types
# stage is one table (asset table in staging schema) and then into 3: asset, asset analytic, asset group (asset schema)


# Import packages, classes and functions
import os
import pandas as pd
import logging
from assetallocation_arp.data_etl import bloomberg_data
# from assetallocation_arp.data_etl import db

# Define logging configuration
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


class ETLProcess:
    def __init__(self):
        self.df_securities = pd.read_csv("instruments_list_snippet.csv")
        self.df_iteration = pd.DataFrame()
        self.df_bbg = pd.DataFrame()

    def bbg_data(self):
        logging.info("Start of module")
        # Call Bloomberg class
        bbg = bloomberg_data.Bloomberg()

        # Get Identifier column from securities data frame
        securities = self.df_securities["Identifier"]

        # Create empty list to append multiple data frames to
        df_list = []
        # Loop through each security and respective fields to get data as a data frame
        for i, security in enumerate(securities, 1):
            self.df_iteration = bbg.historicalRequest(securities=security, fields="PX_LAST", startdate="20200101",
                                                      enddate="20201231")

            # Filter data frame for relevant columns (ticker, value, field, status)
            # self.df_iteration = self.df_iteration[["bbergsymbol", "bbergvalue", "bbergfield", "bbergdate"]]
            # Append data frame to df list
            df_list.append(self.df_iteration)

            logging.info(f"Loop {i}/{len(securities)} complete - \"{security}\" imported as data frame")

        # Concat df list into one large data frame
        self.df_bbg = pd.concat(df_list, axis=0, ignore_index=True)
        logging.info(f"Master data frame created")

        # Output as .csv file
        self.df_bbg.to_csv("out_test.csv", index=False)
        logging.info(f"Master data frame exported as .csv")

        return self.df_bbg

    def clean_data(self):

        # Convert columns to repective format types
        self.df_bbg["bbergsymbol"] = self.df_bbg["bbergsymbol"].astype(str)
        self.df_bbg["bbergfield"] = self.df_bbg["bbergfield"].astype(str)
        self.df_bbg["bbergdate"] = pd.to_datetime(self.df_bbg["bbergdate"])
        self.df_bbg["bbergvalue"] = self.df_bbg["bbergvalue"].astype(float)
        self.df_bbg["status"] = self.df_bbg["status"].astype(str)

        logging.info("Columns converted to respective data types")

        return

    def upload_data(self):

        logging.info("Data written to database")

        return


if __name__ == '__main__':
    etl = ETLProcess()
    etl.bbg_data()
    etl.clean_data()
    etl.upload_data()
