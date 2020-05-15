"""
Created on 12/05/2020
@author: AJ89720
"""

#todo sort the imports
from data_etl.import_data_times import extract_inputs_and_mat_data as data_matlab_effect
from common_libraries.models_names import Models
from models.effect.constants_currencies import Currencies
from common_libraries.names_currencies import CurrencyUSD
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

        start_date = '1999-01-06' # property
        self.data_currencies_usd = self.data_currencies[currencies_usd.currencies_usd_tickers].loc[start_date:]
        self.data_currencies_eur = self.data_currencies[currencies_eur.currencies_eur_tickers].loc[start_date:]


class CurrencyComputations(DataProcessingEffect):

    def __init__(self):
        super().__init__()
        self.carry = pd.DataFrame()
        self.trend = pd.DataFrame()
        self.spot_ex_costs = pd.DataFrame()
        self.spot_incl_costs = pd.DataFrame()

        self.bid_ask_spread = 0
        # Trend
        # Combo
        # Return
        # Return
        # Spot
        # Spot
        # Inflation
        # Inflation

    @property
    def bid_ask(self):
        return self.bid_ask_spread

    @bid_ask.setter
    def bid_ask(self, value):
        self.bid_ask_spread = value

    def carry_computations(self):
        pass

    def trend_computations(self):
        pass

    def spot_ex_costs_computations(self):

        start_date_computations = '2000-01-11' # property
        combo = 1 # to compute self.combo and change it depending on the currency
        currencies = [currency.value for currency in CurrencyUSD] # constant to set
        # loop to get through each currency
        for currency in currencies:
            # Reset the Spot list for the next currency
            spot = [100]  # the Spot is set 100
            spot_division_tmp = (self.data_currencies_usd.loc[start_date_computations:, currency] /
                                 self.data_currencies_usd.loc[start_date_computations:, currency].shift(1))**combo
            # Remove the first nan due to the shift(1)
            spot_division_tmp = spot_division_tmp.iloc[1:]
            # Transform the spot_division_tmp into a list
            spot_tmp = spot_division_tmp.values.tolist()
            # Compute with the previous Spot
            for values in range(len(spot_tmp)):
                spot.append(spot_tmp[values] * spot[values])

            # Store all the spot for each currency
            # spot_ex_costs_tmp = pd.DataFrame(spot, columns=["Spot " + currency])
            self.spot_ex_costs["Spot Ex Costs " + currency] = spot

        # Set the dates to the index of self.spot_ex_costs
        dates_usd = self.data_currencies_usd[start_date_computations:].index.values # property
        self.spot_ex_costs.set_index(dates_usd)

    def spot_incl_computations(self):

        spot = [100]  # the Spot is set 100
        combo = 1 #to compute combo prev and current in the abs
        currencies = [currency.value for currency in CurrencyUSD]
        spot_division_tmp = (self.spot_ex_costs / self.spot_ex_costs.shift(1))*(1-self.bid_ask_spread/20000)**abs(combo)
        # Transform the spot_diviions_tmp into list
        spot_tmp = spot_division_tmp.values.tolist()
        # Compute with the previous Spot
        for values in range(len(spot_tmp)):
            spot.append(spot_tmp[values] * spot[values])


        print()

