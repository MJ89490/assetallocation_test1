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


class DataProcessingEffect:

    def __init__(self, start_date_calculations='2000-01-11'):
        self.obj_import_data = ImportDataEffect()

        self.data_currencies_usd = pd.DataFrame()
        self.data_currencies_eur = pd.DataFrame()

        self.start_date_calculations = start_date_calculations

        self.carry_currencies = pd.DataFrame()
        self.trend_currencies = pd.DataFrame()
        self.spot_ex_costs = pd.DataFrame()
        self.spot_incl_costs = pd.DataFrame()
        self.return_ex_costs = pd.DataFrame()
        self.return_incl_costs = pd.DataFrame()
        self.combo_currencies = pd.DataFrame()

        self.bid_ask_spread = 0

    @property
    def dates_index(self):
        return self.data_currencies_usd.loc[self.start_date_calculations:].index.values

    @property
    def start_date_calculations(self):
        return self._start_date_calculations

    @start_date_calculations.setter
    def start_date_calculations(self, value):
        # todo ADD ERROR HANDLING FOR DATE
        self._start_date_calculations = value

    def data_processing_effect(self):

        obj_currencies = Currencies()
        currencies_usd, currencies_eur = obj_currencies.currencies_data()

        data_currencies = self.obj_import_data.import_data_matlab()

        # start_date = '1999-01-06'
        self.data_currencies_usd = data_currencies[currencies_usd.currencies_usd_tickers].loc[:]
        self.data_currencies_eur = data_currencies[currencies_eur.currencies_eur_tickers].loc[:]

        return self.data_currencies_usd, self.data_currencies_eur

# if __name__ == "__main__":
#     ob = DataProcessingEffect()
#     ob.data_processing_effect()
#     ob.dates_index


# # Using @property decorator
# class Celsius:
#     def __init__(self, temperature=0):
#         self.temperature = temperature
#
#     def to_fahrenheit(self):
#         return (self.temperature * 1.8) + 32
#
#     @property
#     def temperature(self):
#         print("Getting value...")
#         return self._temperature
#
#     @temperature.setter
#     def temperature(self, value):
#         print("Setting value...")
#         if value < -273.15:
#             raise ValueError("Temperature below -273 is not possible")
#         self._temperature = value
#
#
# # create an object
# human = Celsius(37)
#
# print(human.temperature)
#
# print(human.to_fahrenheit())
#
# coldest_thing = Celsius(-300)