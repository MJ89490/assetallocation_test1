"""
Created on 12/05/2020
@author: AJ89720
"""

from models.effect.data_processing_effect import DataProcessingEffect
import models.effect.constants as constants
import pandas as pd
import numpy as np

class CurrencyComputations(DataProcessingEffect):

    def __init__(self):
        super().__init__()
        self.carry = pd.DataFrame()
        self.trend = pd.DataFrame()
        self.spot_ex_costs = pd.DataFrame()
        self.spot_incl_costs = pd.DataFrame()
        self.return_ex_costs = pd.DataFrame()
        self.return_incl_costs = pd.DataFrame()
        self.combo = pd.DataFrame()

        self.bid_ask_spread = 0
        self.start_date_computations = ''

    @property
    def bid_ask(self):
        return self.bid_ask_spread

    @bid_ask.setter
    def bid_ask(self, value):
        self.bid_ask_spread = value

    @property
    def start_date_calculations(self):
        return self.start_date_computations

    @start_date_calculations.setter
    def start_date_calculations(self, value):
        self.start_date_computations = value

    def carry_computations(self, carry_type):

        if carry_type == "Real":  #ENUM

            for currency_spot, currency_implied, currency_carry in zip(constants.CURRENCIES_SPOT, constants.CURRENCIES_IMPLIED, constants.CURRENCIES_CARRY):

                tmp_start_date_computations = self.start_date_computations
                rows = self.data_currencies_usd[tmp_start_date_computations:].shape[0] - 1

                carry = []

                if currency_spot in self.data_currencies_usd.columns:
                    data_all_currencies_spot = self.data_currencies_usd.loc[:, currency_spot].tolist()
                    data_all_currencies_carry = self.data_currencies_usd.loc[:, currency_carry].tolist()
                    data_all_currencies_implied = self.data_currencies_usd.loc[:, currency_implied].tolist()
                    data_all_currencies_index = self.data_currencies_usd.loc[:, 'US0003M Index'].tolist()
                else:
                    data_all_currencies_spot = self.data_currencies_eur.loc[:, currency_spot].tolist()
                    data_all_currencies_carry = self.data_currencies_eur.loc[:, currency_carry].tolist()
                    data_all_currencies_implied = self.data_currencies_eur.loc[:, currency_implied].tolist()
                    data_all_currencies_index = self.data_currencies_eur.loc[:, 'EUR003M Curncy'].tolist()

                for values in range(rows):

                    start_date_index = self.data_currencies_usd.index.get_loc(tmp_start_date_computations)

                    previous_start_date = self.data_currencies_usd.index[start_date_index - 4]
                    previous_four_start_date_index = self.data_currencies_usd.index.get_loc(previous_start_date)

                    average_implied = np.mean(data_all_currencies_implied[previous_four_start_date_index:start_date_index])
                    average_index = np.mean(data_all_currencies_index[previous_four_start_date_index:start_date_index])

                    carry_tmp = ((average_implied - average_index) / 100) - 0.028 #inflation diff

                    if not np.isnan(carry_tmp):
                        carry.append(carry_tmp)
                    else:
                        start_date_index = self.data_currencies_usd.index.get_loc(tmp_start_date_computations)

                        previous_start_date = self.data_currencies_usd.index[start_date_index - 1]
                        previous_start_date_index = self.data_currencies_usd.index.get_loc(previous_start_date)

                        previous_eleven_start_date = self.data_currencies_usd.index[start_date_index - 11]
                        previous_eleven_start_date_index = self.data_currencies_usd.index.get_loc(previous_eleven_start_date)

                        numerator = data_all_currencies_carry[previous_start_date_index] / data_all_currencies_carry[previous_eleven_start_date_index]
                        denominator = data_all_currencies_spot[previous_start_date_index] / data_all_currencies_spot[previous_eleven_start_date_index]

                        carry.append((((numerator / denominator) ** (52/10))-1))

                    tmp_start_date_computations = self.data_currencies_usd.index[start_date_index + 1]

                self.carry['Carry ' + currency_spot] = carry

    def trend_computations(self, trend_ind, short_term, long_term):

        #todo set the dates but décalage avec dates de 1
        if trend_ind == "Total Return": #to change to enum
            currencies = constants.CURRENCIES_SPOT
        else:
            currencies = constants.CURRENCIES_CARRY

        # loop through each date
        for currency in currencies:
            if currency in self.data_currencies_usd.columns:
                trend_short_tmp = self.data_currencies_usd.loc[:, currency].rolling(short_term).mean()
                trend_long_tmp = self.data_currencies_usd.loc[:, currency].rolling(long_term).mean()
            else:
                trend_short_tmp = self.data_currencies_eur.loc[:, currency].rolling(short_term).mean()
                trend_long_tmp = self.data_currencies_eur.loc[:, currency].rolling(long_term).mean()

            self.trend["Trend " + currency] = (trend_short_tmp / trend_long_tmp - 1) * 100

        # loop through each date
        # for currency in currencies:
        #     print(currency)
        #     trend = []
        #     start_date_computations = '2000-01-11'  # property
        #     dates_number = self.data_currencies_usd[start_date_computations:].shape[0]
        #
        #     for date in tqdm(range(dates_number)):
        #
        #         if date == 0:  # init
        #             start_date_loc = self.data_currencies_usd.index.get_loc(start_date_computations)
        #             previous_start_date = self.data_currencies_usd.index[start_date_loc - 1]
        #
        #             trend_short_tmp = self.data_currencies_usd.loc[:previous_start_date, currency][
        #                               -self.short_term:].mean()
        #             t = self.data_currencies_usd.loc[:, currency].rolling(4).mean()
        #
        #             trend_long_tmp = self.data_currencies_usd.loc[:previous_start_date, currency][
        #                              -self.long_term:].mean()
        #
        #             l = self.data_currencies_usd.loc[:, currency].rolling(16).mean()
        #             g = (t / l - 1) * 100
        #         else:
        #             start_date_loc = self.data_currencies_usd.index.get_loc(start_date_computations)
        #             next_start_date = self.data_currencies_usd.index[start_date_loc + 1]
        #             next_start_date_loc = self.data_currencies_usd.index.get_loc(next_start_date)
        #             previous_start_date = self.data_currencies_usd.index[next_start_date_loc - 1]
        #             start_date_computations = next_start_date
        #
        #             trend_short_tmp = self.data_currencies_usd.loc[:previous_start_date, currency][-self.short_term:].mean()
        #             trend_long_tmp = self.data_currencies_usd.loc[:previous_start_date, currency][-self.long_term:].mean()
        #
        #             t = self.data_currencies_usd.loc[:, currency].rolling(4).mean()
        #             l = self.data_currencies_usd.loc[:, currency].rolling(16).mean()
        #
        #             g = (t / l - 1) * 100
        #         trend.append((trend_short_tmp / trend_long_tmp - 1) * 100)
        #
        #     self.trend["Trend " + currency] = trend

    def combo_computations(self, cut_off, incl_shorts, cut_off_s, threshold_for_closing):

        tmp_start_date_computations = self.start_date_computations
        rows = self.data_currencies_usd[tmp_start_date_computations:].shape[0]

        for currency in constants.CURRENCIES_CARRY:
            combo = [0]
            trend = self.trend.loc[tmp_start_date_computations:, 'Trend ' + currency].tolist()
            carry = [0.079] * rows  # set with the correct carry from computations

            for value in range(rows):
                if combo[-1] == 0:
                    if carry[value] >= cut_off and trend[value] >= 0:
                        combo.append(1)
                    else:
                        if incl_shorts == "Yes" and carry[value] <= cut_off and trend[value] <= 0:
                            combo.append(-1)
                        else:
                            combo.append(0)
                else:
                    if carry[value] >= (cut_off - threshold_for_closing) and trend[value] >= 0:
                        combo.append(1)
                    else:
                        if incl_shorts == "Yes" and carry <= (cut_off + threshold_for_closing) and trend[value] <= 0:
                            combo.append(-1)
                        else:
                            combo.append(0)

            self.combo["Combo " + currency] = combo

    def return_ex_costs_computations(self):

        combo = 1

        for currency in constants.CURRENCIES_CARRY:

            first_return = [100]
            if currency in self.data_currencies_usd.columns:
                return_division_tmp = (self.data_currencies_usd.loc[self.start_date_computations:, currency] /
                                       self.data_currencies_usd.loc[self.start_date_computations:, currency].shift(1)) ** combo
            else:
                return_division_tmp = (self.data_currencies_eur.loc[self.start_date_computations:, currency] /
                                       self.data_currencies_eur.loc[self.start_date_computations:, currency].shift(1)) ** combo

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

        combo = 1 # to compute self.combo and change it depending on the currency

        # loop to get through each currency
        for currency in constants.CURRENCIES_SPOT:
            # Reset the Spot list for the next currency
            spot = [100]  # the Spot is set 100
            if currency in self.data_currencies_usd.columns:
                spot_division_tmp = (self.data_currencies_usd.loc[self.start_date_computations:, currency] /
                                     self.data_currencies_usd.loc[self.start_date_computations:, currency].shift(1)) ** combo
            else:
                spot_division_tmp = (self.data_currencies_eur.loc[self.start_date_computations:, currency] /
                                     self.data_currencies_eur.loc[self.start_date_computations:, currency].shift(1)) ** combo

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
        dates_usd = self.data_currencies_usd[self.start_date_computations:].index.values # property
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
