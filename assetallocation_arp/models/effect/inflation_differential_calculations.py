
"""
    Class to make inflation differential calculations
"""

import pandas as pd
from models.effect.inflation_imf_publishing_dates import dates_imf_publishing
from models.effect.data_processing_effect import DataProcessingEffect
from models.effect.effect_model import CurrencyComputations

class InflationDifferential:
    def __init__(self):
        self.inflation_release = pd.Series()

    def inflation_release_computations(self):

        obj_data_processing = DataProcessingEffect()
        obj_data_processing.data_currencies_usd

        dates_index = self.data_currencies_usd.loc[self.start_date_computations:].index.values
        weo_dates = []
        flag = False

        for date_index in dates_index:
            counter = 0
            date_publication = pd.to_datetime(list(dates_imf_publishing)[0], format='%d-%m-%Y')
            date = pd.to_datetime(date_index)
            if date < pd.to_datetime('26-04-2006', format='%d-%m-%Y'):
                weo_date = "Latest"
            else:
                while date > date_publication:
                    counter += 1
                    if counter >= len(dates_imf_publishing):
                        # Reach the end of the dates publishing dates
                        flag = True
                        break
                    date_publication = pd.to_datetime(list(dates_imf_publishing)[counter], format='%d-%m-%Y')
                else:
                    weo_date = list(dates_imf_publishing)[counter - 1]
                    weo_date = dates_imf_publishing[weo_date]

            if flag:
                weo_date = list(dates_imf_publishing)[-1]
                weo_date = dates_imf_publishing[weo_date]
                flag = False

            weo_dates.append(weo_date)

        self.inflation_release["Inflation Release"] = weo_dates
        # Set the index and shift the data by one
        self.inflation_release = self.inflation_release.set_index(dates_index).shift(1)
        # Replace the nan by Latest because we know it is the only nan in the Series
        self.inflation_release = self.inflation_release.fillna('Latest')

    def inflation_differential_download(self):
        pass

    def inflation_differential_computations(self):
        pass