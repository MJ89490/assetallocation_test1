from data_etl.import_data_times import extract_inputs_and_mat_data as data_matlab_effect
from common_libraries.constants_currencies import Currencies
from common_libraries.models_names import Models

import pandas as pd


class ImportDataEffect:

    def __init__(self):
        self.data_currencies = pd.DataFrame()

    def import_data_matlab(self):
        self.data_currencies = data_matlab_effect(model_type=Models.effect.name, mat_file=None,
                                                  input_file=None, date=None)

        return self.data_currencies


class ProcessDataEffect:

    def __init__(self, start_date_calculations='2000-01-11'):
        self.obj_import_data = ImportDataEffect()

        self.data_currencies_usd = pd.DataFrame()
        self.data_currencies_eur = pd.DataFrame()

        self.start_date_calculations = start_date_calculations

    @property
    def dates_index(self):
        start_current_date_index_loc = self.data_currencies_usd.index.get_loc(self.start_date_calculations)
        new_start_date_index = self.data_currencies_usd.index[start_current_date_index_loc - 1]

        return self.data_currencies_usd.loc[new_start_date_index:].index.values

    @property
    def dates_origin_index(self):
        return self.data_currencies_usd.loc[self.start_date_calculations:].index.values

    @property
    def start_date_calculations(self):
        return self._start_date_calculations

    @start_date_calculations.setter
    def start_date_calculations(self, value):
        # todo ADD ERROR HANDLING FOR DATE
        self._start_date_calculations = value

    def process_data_effect(self):

        obj_currencies = Currencies()
        currencies_usd, currencies_eur = obj_currencies.currencies_data()

        data_currencies = self.obj_import_data.import_data_matlab()

        # start_date = '1999-01-06'
        self.data_currencies_usd = data_currencies[currencies_usd.currencies_usd_tickers].loc[:]
        self.data_currencies_eur = data_currencies[currencies_eur.currencies_eur_tickers].loc[:]

        return self.data_currencies_usd, self.data_currencies_eur
