# Import packages, classes and functions
import os
import pandas as pd
import logging
from datetime import datetime, timedelta
import bloomberg_data
from db import Db

# Define logging configuration
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


class ETLProcess:
    def __init__(self, df_input):
        self.df_input = df_input
        self.df_iteration = pd.DataFrame()
        self.df_bbg = pd.DataFrame()

    def clean_input(self):
        # Convert columns to respective format types
        self.df_input["ticker"] = self.df_input["ticker"].astype(str)
        self.df_input["name"] = self.df_input["name"].astype(str)
        self.df_input["description"] = self.df_input["description"].astype(str)
        self.df_input["asset_category"] = self.df_input["asset_category"].astype(str)
        self.df_input["asset_subcategory"] = self.df_input["asset_subcategory"].astype(str)
        self.df_input["currency"] = self.df_input["currency"].astype(str)
        self.df_input["country"] = self.df_input["country"].astype(str)
        self.df_input["is_tr"] = self.df_input["is_tr"].astype(str)
        self.df_input["analytic_category"] = self.df_input["analytic_category"].astype(str)
        self.df_input["business_datetime"] = datetime(1900, 1, 1).strftime('%Y%m%d')

        return self.df_input

    def bbg_data(self):
        logging.info("Start of module")
        # Call Bloomberg class
        # Create empty list to append multiple data frames to
        bbg = bloomberg_data.Bloomberg()
        df_list = []
        # Loop through each security and respective fields to get data as a data frame
        for index, row in self.df_input.iterrows():
            self.df_iteration = bbg.historicalRequest(securities=row["ticker"],
                                                      fields=row["description"],
                                                      startdate=row["business_datetime"],
                                                      enddate=(datetime.today() - timedelta(days=1)).strftime('%Y%m%d'))

            # Append data frame to df list
            df_list.append(self.df_iteration)

            logging.info(f"Loop {index}/{len(self.df_input.index)} complete - \"{row['ticker']}\" imported as data frame")

        # Concat df list into one large data frame
        self.df_bbg = pd.concat(df_list, axis=0, ignore_index=True)
        logging.info(f"Master data frame created")

        return self.df_bbg

    def clean_data(self):

        # Rename column headers to match table in database
        col_dict = {'bbergsymbol': 'ticker',
                    'bbergfield': 'description',
                    'bbergdate': 'business_datetime',
                    'bbergvalue': 'value',
                    'status': 'source'}
        self.df_bbg.columns = [col_dict.get(x, x) for x in self.df_bbg.columns]

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

        logging.info("Columns converted to respective data types")

        return self.df_bbg

    def upload_data(self):

        # Call function that uploads data frame to SQL database from respective class
        db = Db()
        db.df_to_staging_asset(self.df_bbg)

        logging.info("Data written to database")

        return
