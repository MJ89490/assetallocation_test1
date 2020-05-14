"""
Created on 12/05/2020
@author: AJ89720
"""

#todo sort the imports
from data_etl.import_data_times import extract_inputs_and_mat_data as data_matlab_effect
from common_libraries.models_names import Models
from models.effect.constants_currencies import Currencies
import pandas as pd


class ImportDataEffect:

    def __init__(self):
        self.data_currencies = pd.DataFrame()

    def import_data_matlab(self):
        self.data_currencies = data_matlab_effect(model_type=Models.effect.name, mat_file=None,
                                                  input_file=None, model_date=None)


class DataProcessingEffect(ImportDataEffect):

    def __init__(self):
        super().__init__()
        self.data_currencies_usd = pd.DataFrame()
        self.data_currencies_eur = pd.DataFrame()

    def data_processing_effect(self):

        #todo : ask to Simone US0003M Curncy # "RONEURCR Curncy", 'ILSUSDCR Curncy', EGPUSDCR Curncy', 'NNNI3M Index', 'NGNUSDCR Curncy' not available in matlab file

        obj_currencies = Currencies()
        currencies_usd, currencies_eur = obj_currencies.currencies_data()

        start_date = '1999-01-06' #property
        self.data_currencies_usd = self.data_currencies[currencies_usd.currencies_usd_tickers].loc[start_date:]
        self.data_currencies_eur = self.data_currencies[currencies_eur.currencies_eur_tickers].loc[start_date:]


class CurrencyComputations(DataProcessingEffect):
    def __init__(self):
        super().__init__()
        self.carry = pd.DataFrame()
        self.trend = pd.DataFrame()
        self.spot_ex_costs = pd.DataFrame()
        # Trend
        # Combo
        # Return
        # Return
        # Spot
        # Spot
        # Inflation
        # Inflation


    def carry_computations(self):
        pass

    def trend_computations(self):
        pass

    def spot_ex_costs_computations(self):

        start_date_computations = '2000-01-12' #property

        dates = self.data_currencies_usd.index.values # property

        spot = pd.Series([100] * len(dates), index=dates)

        # spot = spot.set_index(dates)

        #todo Target the Spot column for each currency in self.data_currencies_usd to compute spot ex costs
        combo = 1 # to compute
        spot = spot.loc[start_date_computations:].shift(1) * (self.data_currencies_usd.loc[start_date_computations:, 'BRLUSD Curncy'] / self.data_currencies_usd.loc[start_date_computations:, 'BRLUSD Curncy'].shift(1))**(combo)

        l = spot.loc[start_date_computations:].shift(1) * p

        #todo create a loop to compute the previous spot with the current one

        spot = spot / spot.shift(1)


        o = pd.DataFrame([1.006068408, 1.020654359, 1.006805158])

        m = pd.DataFrame([100, 100, 100])

        l =  o * m.shift(1)


if __name__=="__main__":
    obj_import_data = ImportDataEffect()
    obj_import_data.import_data_matlab()

