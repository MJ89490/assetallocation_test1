"""
Created on 12/05/2020
@author: AJ89720
"""

#todo sort the imports
from data_etl.import_data_times import extract_inputs_and_mat_data as data_matlab_effect
from common_libraries.models_names import Models
from models.effect.constants_currencies import Currencies
from common_libraries.names_currencies_spot import CurrencyUSDSpot
from common_libraries.names_currencies_carry import CurrencyUSDCarry
import pandas as pd


class ImportDataEffect:

    def __init__(self):
        self.data_currencies = pd.DataFrame()

    def import_data_matlab(self):
        self.data_currencies = data_matlab_effect(model_type=Models.effect.name, mat_file=None,
                                                  input_file=None, date=None)


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
        self.return_ex_costs = pd.DataFrame()
        self.return_incl_costs = pd.DataFrame()

        self.bid_ask_spread = 0
        self.cut_off_long = 0
        self.shorts = ""
        self.threshold_for_closing = 0
        self.trend_ind = ""
        self.short_term = 0
        self.long_term = 0

    @property
    def bid_ask(self):
        return self.bid_ask_spread

    @bid_ask.setter
    def bid_ask(self, value):
        self.bid_ask_spread = value

    @property
    def cut_off(self):
        return self.cut_off_long

    @cut_off.setter
    def cut_off(self, value):
        self.cut_off_long = value

    @property
    def incl_shorts(self):
        return self.shorts

    @incl_shorts.setter
    def incl_shorts(self, value):
        self.shorts = value

    @property
    def threshold(self):
        return self.threshold_for_closing

    @threshold.setter
    def threshold(self, value):
        self.threshold_for_closing = value

    @property
    def trend_indicator(self):
        return self.trend_ind

    @trend_indicator.setter
    def trend_indicator(self, value):
        self.trend_ind = value

    @property
    def short_term_ma(self):
        return self.short_term

    @short_term_ma.setter
    def short_term_ma(self, value):
        self.short_term = value

    @property
    def long_term_ma(self):
        return self.long_term

    @long_term_ma.setter
    def long_term_ma(self, value):
        self.long_term = value

    def carry_computations(self):
        pass

    def trend_computations(self):

        start_date_computations = '2000-01-11'  # property


        import datetime

        dates_number = self.data_currencies_usd[start_date_computations:].shape[0]
        # dates_usd = self.data_currencies_usd+[start_date_computations:].index.values.tolist()  # property
        # loop through each date
        # dates_usd = self.data_currencies_usd.index.get_loc(start_date_computations)

        for date in range(dates_number):

            if date == 0:  # init
                start_date_loc = self.data_currencies_usd.index.get_loc(start_date_computations)
                previous_start_date = self.data_currencies_usd.index[start_date_loc - 1]

                trend_short_tmp = self.data_currencies_usd.loc[:previous_start_date, "BRLUSD Curncy"][
                                  -self.short_term:].mean()
                trend_long_tmp = self.data_currencies_usd.loc[:previous_start_date, "BRLUSD Curncy"][
                                 -self.long_term:].mean()

            else:
                start_date_loc = self.data_currencies_usd.index.get_loc(start_date_computations)
                next_start_date = self.data_currencies_usd.index[start_date_loc + 1]
                previous_start_date = self.data_currencies_usd.index[next_start_date - 1]
                start_date_computations = next_start_date

                trend_short_tmp = self.data_currencies_usd.loc[:previous_start_date, "BRLUSD Curncy"][-self.short_term:].mean()
                trend_long_tmp = self.data_currencies_usd.loc[:previous_start_date, "BRLUSD Curncy"][-self.long_term:].mean()

            self.trend["Trend " + "BRLUSD Curncy"] = (trend_short_tmp / trend_long_tmp - 1) * 100



        # start_date_computations_obj = datetime.datetime.strptime(start_date_computations, '%Y-%m-%d')
        # start_date_computations_obj = start_date_computations_obj.date() - datetime.timedelta(1)









    def combo_computations(self):
        pass

    def return_ex_costs_computations(self):

        start_date_computations = '2000-01-11'  # property
        combo = 1
        currencies = [currency.value for currency in CurrencyUSDCarry]

        for currency in currencies:

            first_return = [100]
            return_division_tmp = (self.data_currencies_usd.loc[start_date_computations:, currency] /
                                   self.data_currencies_usd.loc[start_date_computations:, currency].shift(1)) ** combo
            return_division_tmp = return_division_tmp.iloc[1:]
            return_tmp = return_division_tmp.tolist()
            for values in range(len(return_tmp)):
                first_return.append(return_tmp[values] * first_return[values])

            self.return_ex_costs["Return Ex Costs " + currency] = first_return

        # todo set the dates

    def return_incl_costs_computations(self):

        combo = 1
        returns_division_tmp = self.return_ex_costs / self.return_ex_costs.shift(1) * (1-self.bid_ask_spread/20000) ** abs(combo)

        returns_division_tmp = returns_division_tmp.iloc[1:]

        currency_ex_costs = returns_division_tmp.columns.values.tolist()

        for name in currency_ex_costs:
            first_return = [100]
            return_tmp = returns_division_tmp[name].tolist()
            for values in range(len(return_tmp)):
                first_return.append(return_tmp[values] * first_return[values])

            self.return_incl_costs[name.replace("Return Ex Costs", "Return Incl Costs")] = first_return

        # todo set the dates

    def spot_ex_costs_computations(self):

        start_date_computations = '2000-01-11' # property
        combo = 1 # to compute self.combo and change it depending on the currency
        currencies = [currency.value for currency in CurrencyUSDSpot] # constant to set
        # loop to get through each currency
        for currency in currencies:
            # Reset the Spot list for the next currency
            spot = [100]  # the Spot is set 100
            spot_division_tmp = (self.data_currencies_usd.loc[start_date_computations:, currency] /
                                 self.data_currencies_usd.loc[start_date_computations:, currency].shift(1)) ** combo
            # Remove the first nan due to the shift(1)
            spot_division_tmp = spot_division_tmp.iloc[1:]
            # Transform the spot_division_tmp into a list
            spot_tmp = spot_division_tmp.values.tolist()
            # Compute with the previous Spot
            for values in range(len(spot_tmp)):
                spot.append(spot_tmp[values] * spot[values])

            # Store all the spot for each currency
            self.spot_ex_costs["Spot Ex Costs " + currency] = spot

        # Set the dates to the index of self.spot_ex_costs
        dates_usd = self.data_currencies_usd[start_date_computations:].index.values # property
        self.spot_ex_costs.set_index(dates_usd)

    def spot_incl_computations(self):

        combo = 1 #to compute combo prev and current in the abs
        spot_division_tmp = (self.spot_ex_costs / self.spot_ex_costs.shift(1))*(1-self.bid_ask_spread/20000)**abs(combo)

        # Remove the first nan due to the shift(1)
        spot_division_tmp = spot_division_tmp.iloc[1:]

        currency_ex_costs = spot_division_tmp.columns.values.tolist() # set to global name

        # loop through each currency in spot_division_tmp
        for name in currency_ex_costs:
            spot = [100]  # the Spot is set 100
            spot_tmp = spot_division_tmp[name].tolist()
            # Compute with the previous Spot
            for values in range(len(spot_tmp)):
                spot.append(spot_tmp[values] * spot[values])

            self.spot_incl_costs[name.replace("Spot Ex Costs", "Spot Incl Costs")] = spot

        # todo set the dates to the index of self.spot_incl_costs
        print()

