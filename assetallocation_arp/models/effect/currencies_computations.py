"""
Created on 12/05/2020
@author: AJ89720
"""

from assetallocation_arp.models.effect.data_effect import DataProcessingEffect
from assetallocation_arp.common_libraries.names_columns_dataframe import CurrencySpot
import common_libraries.constants as constants
from common_libraries.names_currencies_implied import CurrencyBaseImplied
import pandas as pd
import numpy as np


class CurrencyComputations(DataProcessingEffect):

    # def __init__(self):
    #     super().__init__()
    #
    #     self.carry_currencies = pd.DataFrame()
    #     self.trend_currencies = pd.DataFrame()
    #     self.spot_ex_costs = pd.DataFrame()
    #     self.spot_incl_costs = pd.DataFrame()
    #     self.return_ex_costs = pd.DataFrame()
    #     self.return_incl_costs = pd.DataFrame()
    #     self.combo_currencies = pd.DataFrame()
    #
    #     # self.start_date_computations = start_date_computations
    #
    #     # self.data_currencies_usd, self.data_currencies_eur = self.data_processing_effect()
    #     self.bid_ask_spread = 0

    @property
    def bid_ask(self):
        return self.bid_ask_spread

    @bid_ask.setter
    def bid_ask(self, value):
        self.bid_ask_spread = value

    def carry_computations(self, carry_type, inflation_differential):

        if carry_type.lower() == 'real':

            for currency_spot, currency_implied, currency_carry in \
                    zip(constants.CURRENCIES_SPOT, constants.CURRENCIES_IMPLIED, constants.CURRENCIES_CARRY):

                tmp_start_date_computations = self.start_date_calculations

                rows = self.data_currencies_usd[tmp_start_date_computations:].shape[0]

                carry = []

                if currency_spot in constants.CURRENCIES_SPOT:
                    data_all_currencies_spot = self.data_currencies_usd.loc[:, currency_spot].tolist()
                    data_all_currencies_carry = self.data_currencies_usd.loc[:, currency_carry].tolist()
                    data_all_currencies_implied = self.data_currencies_usd.loc[:, currency_implied].tolist()
                    data_all_currencies_index = self.data_currencies_usd.loc[:, CurrencyBaseImplied.US0003M.value].tolist()
                else:
                    data_all_currencies_spot = self.data_currencies_eur.loc[:, currency_spot].tolist()
                    data_all_currencies_carry = self.data_currencies_eur.loc[:, currency_carry].tolist()
                    data_all_currencies_implied = self.data_currencies_eur.loc[:, currency_implied].tolist()
                    data_all_currencies_index = self.data_currencies_eur.loc[:, CurrencyBaseImplied.EUR003M.value].tolist()

                for values in range(rows):

                    start_date_index_loc = self.data_currencies_usd.index.get_loc(tmp_start_date_computations)

                    start_date_index = pd.to_datetime(self.data_currencies_usd.index[start_date_index_loc],
                                                      format='%d-%m-%Y')

                    previous_start_date = self.data_currencies_usd.index[start_date_index_loc - 4]
                    previous_four_start_date_index = self.data_currencies_usd.index.get_loc(previous_start_date)

                    average_implied = np.mean(data_all_currencies_implied[previous_four_start_date_index:start_date_index_loc])
                    average_index = np.mean(data_all_currencies_index[previous_four_start_date_index:start_date_index_loc])

                    carry_tmp = ((average_implied - average_index) / 100) - inflation_differential.loc[start_date_index][0]
                    print(start_date_index)
                    if not np.isnan(carry_tmp):
                        carry.append(carry_tmp)
                    else:
                        start_date_index_loc = self.data_currencies_usd.index.get_loc(tmp_start_date_computations)

                        previous_start_date = self.data_currencies_usd.index[start_date_index_loc - 1]
                        previous_start_date_index = self.data_currencies_usd.index.get_loc(previous_start_date)

                        previous_eleven_start_date = self.data_currencies_usd.index[start_date_index_loc - 11]
                        previous_eleven_start_date_index = self.data_currencies_usd.index.get_loc(previous_eleven_start_date)

                        numerator = data_all_currencies_carry[previous_start_date_index] / data_all_currencies_carry[previous_eleven_start_date_index]
                        denominator = data_all_currencies_spot[previous_start_date_index] / data_all_currencies_spot[previous_eleven_start_date_index]

                        carry.append((((numerator / denominator) ** (52/10))-1))

                    try:
                        tmp_start_date_computations = self.data_currencies_usd.index[start_date_index_loc + 1]
                    except IndexError:
                        tmp_start_date_computations = self.data_currencies_usd.index[start_date_index_loc]

                self.carry_currencies[CurrencySpot.Carry.name + currency_spot] = carry

            self.carry_currencies = self.carry_currencies.set_index(self.dates_index)

    def trend_computations(self, trend_ind, short_term, long_term):

        if trend_ind.lower() == 'total return':
            currencies = constants.CURRENCIES_CARRY
        else:
            currencies = constants.CURRENCIES_SPOT

        # loop through each date
        for currency, currency_name_col in zip(currencies, constants.CURRENCIES_SPOT):
            if currency in self.data_currencies_usd.columns:
                trend_short_tmp = self.data_currencies_usd.loc[:, currency].rolling(short_term).mean()
                trend_long_tmp = self.data_currencies_usd.loc[:, currency].rolling(long_term).mean()
            else:
                trend_short_tmp = self.data_currencies_eur.loc[:, currency].rolling(short_term).mean()
                trend_long_tmp = self.data_currencies_eur.loc[:, currency].rolling(long_term).mean()

            self.trend_currencies[CurrencySpot.Trend.name + currency_name_col] = ((trend_short_tmp / trend_long_tmp)-1)*100

        # take the previous date compared to self.date_computations because there is a shift of 1 because of rolling
        start_date_loc = self.data_currencies_usd.index.get_loc(self.start_date_calculations)
        previous_start_date = self.data_currencies_usd.index[start_date_loc - 1]

        self.trend_currencies = self.trend_currencies[previous_start_date:].iloc[:-1]
        self.trend_currencies = self.trend_currencies.set_index(self.dates_index)

    def combo_computations(self, cut_off, incl_shorts, cut_off_s, threshold_for_closing):

        tmp_start_date_computations = self.start_date_calculations
        rows = self.data_currencies_usd[tmp_start_date_computations:].shape[0]

        for currency_spot in constants.CURRENCIES_SPOT:
            # set the combo to zero as first value
            combo = [0]
            trend = self.trend_currencies.loc[tmp_start_date_computations:, CurrencySpot.Trend.name + currency_spot].tolist()
            carry = self.carry_currencies.loc[tmp_start_date_computations:, CurrencySpot.Carry.name + currency_spot].tolist()

            for value in range(rows):
                if combo[-1] == 0:
                    if carry[value] >= cut_off and trend[value] >= 0:
                        combo.append(1)
                    else:
                        if incl_shorts.lower() == 'yes' and carry[value] <= cut_off_s and trend[value] <= 0:
                            combo.append(-1)
                        else:
                            combo.append(0)
                else:
                    if carry[value] >= (cut_off - threshold_for_closing) and trend[value] >= 0:
                        combo.append(1)
                    else:
                        if incl_shorts.lower() == 'yes' and carry[value] <= (cut_off_s + threshold_for_closing) and trend[value] <= 0:
                            combo.append(-1)
                        else:
                            combo.append(0)

            self.combo_currencies[CurrencySpot.Combo.name + currency_spot] = combo

        # remove the first line as it was the initialization of the combo
        self.combo_currencies = self.combo_currencies.iloc[1:]
        self.combo_currencies = self.combo_currencies.set_index(self.dates_index)

    def return_ex_costs_computations(self):

        for currency_carry, currency_spot in zip(constants.CURRENCIES_CARRY, constants.CURRENCIES_SPOT):

            first_return = [100]

            if currency_carry in self.data_currencies_usd.columns:
                return_division_tmp = (self.data_currencies_usd.loc[self.start_date_calculations:, currency_carry] /
                                       self.data_currencies_usd.loc[self.start_date_calculations:, currency_carry].shift(1))
            else:
                return_division_tmp = (self.data_currencies_eur.loc[self.start_date_calculations:, currency_carry] /
                                       self.data_currencies_eur.loc[self.start_date_calculations:, currency_carry].shift(1))

            combo_tmp = self.combo_currencies[CurrencySpot.Combo.name + currency_spot].tolist()
            combo_tmp.pop(0)
            return_division_tmp = return_division_tmp.iloc[1:]
            return_tmp = return_division_tmp.tolist()

            for values in range(len(return_tmp)):
                first_return.append(first_return[values] * return_tmp[values] ** combo_tmp[values])

            self.return_ex_costs[CurrencySpot.Return_Ex_Costs.name + currency_spot] = first_return

        self.return_ex_costs = self.return_ex_costs.set_index(self.dates_index)

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

            self.return_incl_costs[name.replace(CurrencySpot.Return_Ex_Costs.name,
                                                CurrencySpot.Return_Incl_Costs.name)] = first_return

        self.return_incl_costs = self.return_incl_costs.set_index(self.dates_index)

    def spot_ex_costs_computations(self):

        # loop to get through each currency
        for currency in constants.CURRENCIES_SPOT:
            # Reset the Spot list for the next currency
            spot = [100]  # the Spot is set 100
            if currency in self.data_currencies_usd.columns:
                spot_division_tmp = (self.data_currencies_usd.loc[self.start_date_calculations:, currency] /
                                     self.data_currencies_usd.loc[self.start_date_calculations:, currency].shift(1))
            else:
                spot_division_tmp = (self.data_currencies_eur.loc[self.start_date_calculations:, currency] /
                                     self.data_currencies_eur.loc[self.start_date_calculations:, currency].shift(1))

            combo_tmp = self.combo_currencies.loc[self.start_date_calculations:, CurrencySpot.Combo.name + currency].tolist()
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
            self.spot_ex_costs[CurrencySpot.Spot_Ex_Costs.name + currency] = spot

        # Set the dates to the index of self.spot_ex_costs
        self.spot_ex_costs = self.spot_ex_costs.set_index(self.dates_index)

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

            self.spot_incl_costs[name.replace(CurrencySpot.Spot_Ex_Costs.name,
                                              CurrencySpot.Spot_Incl_Costs.name)] = spot

        # set the dates to the index of self.spot_incl_costs
        self.spot_incl_costs = self.spot_incl_costs.set_index(self.dates_index)
