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
        self.carry_currencies = pd.DataFrame()
        self.trend_currencies = pd.DataFrame()
        self.spot_ex_costs = pd.DataFrame()
        self.spot_incl_costs = pd.DataFrame()
        self.return_ex_costs = pd.DataFrame()
        self.return_incl_costs = pd.DataFrame()
        self.combo_currencies = pd.DataFrame()
        self.inflation_release = pd.DataFrame()

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

    def inflation_release_computations(self):
        dates_index = self.data_currencies_usd.loc[self.start_date_computations:].index.values
        weo_dates = []

        for date in dates_index:
            date = pd.to_datetime(date)
            if date.month < 4:
                weo_date = "{month}{year}".format(year=date.year - 1, month='Oct')
            elif date.month == 4 and date.day <= 15:
                weo_date = "{month}{year}".format(year=date.year - 1, month='Oct')
            elif date.month >= 4 and date.month < 10:
                weo_date = "{month}{year}".format(year=date.year, month='Apr')
            else:
                assert date.month >= 10, date
                weo_date = "{month}{year}".format(year=date.year, month='Oct')

            weo_dates.append(weo_date)

        self.inflation_release["Inflation Release"] = weo_dates

    def carry_computations(self, carry_type):

        if carry_type == "Real":  #ENUM

            for currency_spot, currency_implied, currency_carry in zip(constants.CURRENCIES_SPOT, constants.CURRENCIES_IMPLIED, constants.CURRENCIES_CARRY):

                tmp_start_date_computations = self.start_date_computations

                rows = self.data_currencies_usd[tmp_start_date_computations:].shape[0]

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

                    try:
                        tmp_start_date_computations = self.data_currencies_usd.index[start_date_index + 1]
                    except IndexError:
                        tmp_start_date_computations = self.data_currencies_usd.index[start_date_index]

                self.carry_currencies['Carry ' + currency_spot] = carry

        dates_usd = self.data_currencies_usd[self.start_date_computations:].index.values  # property
        self.carry_currencies = self.carry_currencies.set_index(dates_usd)

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

            self.trend_currencies["Trend " + currency] = (trend_short_tmp / trend_long_tmp - 1) * 100

        self.trend_currencies = self.trend_currencies.loc[self.start_date_computations:]

    def combo_computations(self, cut_off, incl_shorts, cut_off_s, threshold_for_closing):

        tmp_start_date_computations = self.start_date_computations
        rows = self.data_currencies_usd[tmp_start_date_computations:].shape[0]

        for currency_carry, currency_spot in zip(constants.CURRENCIES_CARRY, constants.CURRENCIES_SPOT):
            combo = [0] # set the combo to zero as first value
            trend = self.trend_currencies.loc[tmp_start_date_computations:, 'Trend ' + currency_carry].tolist()
            carry = self.carry_currencies.loc[tmp_start_date_computations:, 'Carry ' + currency_spot].tolist()

            for value in range(rows):
                if combo[-1] == 0:
                    if carry[value] >= cut_off and trend[value] >= 0:
                        combo.append(1)
                    else:
                        if incl_shorts == "Yes" and carry[value] <= cut_off_s and trend[value] <= 0:
                            combo.append(-1)
                        else:
                            combo.append(0)
                else:
                    if carry[value] >= (cut_off - threshold_for_closing) and trend[value] >= 0:
                        combo.append(1)
                    else:
                        if incl_shorts == "Yes" and carry <= (cut_off_s + threshold_for_closing) and trend[value] <= 0:
                            combo.append(-1)
                        else:
                            combo.append(0)

            self.combo_currencies["Combo " + currency_spot] = combo

        dates_usd = self.data_currencies_usd[self.start_date_computations:].index.values  # property
        self.combo_currencies = self.combo_currencies.iloc[1:]  # remove the first line as it was the initialization of the combo
        self.combo_currencies = self.combo_currencies.set_index(dates_usd)

    def return_ex_costs_computations(self):

        for currency_carry, currency_spot in zip(constants.CURRENCIES_CARRY, constants.CURRENCIES_SPOT):

            first_return = [100]

            if currency_carry in self.data_currencies_usd.columns:
                return_division_tmp = (self.data_currencies_usd.loc[self.start_date_computations:, currency_carry] /
                                       self.data_currencies_usd.loc[self.start_date_computations:, currency_carry].shift(1))
            else:
                return_division_tmp = (self.data_currencies_eur.loc[self.start_date_computations:, currency_carry] /
                                       self.data_currencies_eur.loc[self.start_date_computations:, currency_carry].shift(1))

            combo_tmp = self.combo_currencies["Combo " + currency_spot].tolist()
            combo_tmp.pop(0)
            return_division_tmp = return_division_tmp.iloc[1:]
            return_tmp = return_division_tmp.tolist()

            for values in range(len(return_tmp)):
                first_return.append(first_return[values] * return_tmp[values] ** combo_tmp[values])

            self.return_ex_costs["Return Ex Costs " + currency_spot] = first_return

        dates_usd = self.data_currencies_usd[self.start_date_computations:].index.values # property
        self.return_ex_costs = self.return_ex_costs.set_index(dates_usd)

    def return_incl_costs_computations(self):

        returns_division_tmp = self.return_ex_costs / self.return_ex_costs.shift(1) * (1-self.bid_ask_spread/20000)

        returns_division_tmp = returns_division_tmp.iloc[1:]

        currency_ex_costs = returns_division_tmp.columns.values.tolist()
        combo_names = self.combo_currencies.columns.tolist()

        for name, combo_name in zip(currency_ex_costs, combo_names):
            first_return = [100]
            return_tmp = returns_division_tmp[name].tolist()
            combo_tmp = self.combo_currencies[combo_name].tolist()
            combo_tmp.pop(0)
            for values in range(len(return_tmp)):
                first_return.append(first_return[values] * return_tmp[values] ** combo_tmp[values])

            self.return_incl_costs[name.replace("Return Ex Costs", "Return Incl Costs")] = first_return

        dates_usd = self.data_currencies_usd[self.start_date_computations:].index.values # property
        self.return_incl_costs = self.return_incl_costs.set_index(dates_usd)

    def spot_ex_costs_computations(self):

        # loop to get through each currency
        for currency in constants.CURRENCIES_SPOT:
            # Reset the Spot list for the next currency
            spot = [100]  # the Spot is set 100
            if currency in self.data_currencies_usd.columns:
                spot_division_tmp = (self.data_currencies_usd.loc[self.start_date_computations:, currency] /
                                     self.data_currencies_usd.loc[self.start_date_computations:, currency].shift(1))
            else:
                spot_division_tmp = (self.data_currencies_eur.loc[self.start_date_computations:, currency] /
                                     self.data_currencies_eur.loc[self.start_date_computations:, currency].shift(1))

            combo_tmp = self.combo_currencies.loc[self.start_date_computations:, 'Combo ' + currency].tolist()
            # Remove the first line to be equal with the spot_tmp
            combo_tmp.pop(0)
            # Remove the first nan due to the shift(1)
            spot_division_tmp = spot_division_tmp.iloc[1:]
            # Transform the spot_division_tmp into a list
            spot_tmp = spot_division_tmp.values.tolist()
            # Compute with the previous Spot
            for value in range(len(spot_tmp)):
                spot.append(spot[value] * spot_tmp[value] ** combo_tmp[value])

            # Store all the spot for each currency
            self.spot_ex_costs["Spot Ex Costs " + currency] = spot

        # Set the dates to the index of self.spot_ex_costs
        dates_usd = self.data_currencies_usd[self.start_date_computations:].index.values # property
        self.spot_ex_costs = self.spot_ex_costs.set_index(dates_usd)

    def spot_incl_computations(self):

        combo = abs(self.combo_currencies-self.combo_currencies.shift(1))

        spot_division_tmp = self.spot_ex_costs / self.spot_ex_costs.shift(1)*(1-self.bid_ask_spread/20000)

        # Remove the first nan due to the shift(1)
        spot_division_tmp = spot_division_tmp.iloc[1:]
        combo = combo.iloc[1:]

        currency_ex_costs = spot_division_tmp.columns.values.tolist()
        combo_names = combo.columns.tolist()

        # loop through each currency in spot_division_tmp
        for name, combo_name in zip(currency_ex_costs, combo_names):
            spot = [100]  # the Spot is set 100
            spot_tmp = spot_division_tmp[name].tolist()
            combo_tmp = combo[combo_name].tolist()
            # Compute with the previous Spot
            for values in range(len(spot_tmp)):
                spot.append(spot[values] * spot_tmp[values] ** combo_tmp[values])

            self.spot_incl_costs[name.replace("Spot Ex Costs", "Spot Incl Costs")] = spot

        # set the dates to the index of self.spot_incl_costs
        dates_usd = self.data_currencies_usd[self.start_date_computations:].index.values # property
        self.spot_incl_costs = self.spot_incl_costs.set_index(dates_usd)
