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

        self.data_currencies_usd = self.data_currencies[currencies_usd.currencies_usd_tickers]
        self.data_currencies_eur = self.data_currencies[currencies_eur.currencies_eur_tickers]



    #todo : do the same as TIMES model


class CurrencyComputations:
    def __init__(self):
        pass
        # Carry
        # Trend
        # Combo
        # Return
        # Return
        # Spot
        # Spot
        # Inflation
        # Inflation

    #properties = inputs?

if __name__=="__main__":
    obj_import_data = ImportDataEffect()
    obj_import_data.import_data_matlab()

