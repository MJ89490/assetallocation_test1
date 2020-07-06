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

#todo transformer date en timestamp dans la property
#todo  modifier propriétés!!
class CurrencyComputations(DataProcessingEffect):

    @property
    def bid_ask(self):
        return self.bid_ask_spread

    @bid_ask.setter
    def bid_ask(self, value):
        self.bid_ask_spread = value

    def compute_carry(self, carry_type, inflation_differential):

        for currency_spot, currency_implied, currency_carry in \
                zip(constants.CURRENCIES_SPOT, constants.CURRENCIES_IMPLIED, constants.CURRENCIES_CARRY):

            tmp_start_date_computations = self.start_date_calculations

            rows = self.data_currencies_usd[tmp_start_date_computations:].shape[0]

            carry = []

            if currency_spot in constants.CURRENCIES_SPOT:
                data_all_currencies_spot = self.data_currencies_usd.loc[:, currency_spot].tolist()
                data_all_currencies_carry = self.data_currencies_usd.loc[:, currency_carry].tolist()
                data_all_currencies_implied = self.data_currencies_usd.loc[:, currency_implied].tolist()
                data_all_currencies_implied_base = self.data_currencies_usd.loc[:, CurrencyBaseImplied.US0003M.value].tolist()
            else:
                data_all_currencies_spot = self.data_currencies_eur.loc[:, currency_spot].tolist()
                data_all_currencies_carry = self.data_currencies_eur.loc[:, currency_carry].tolist()
                data_all_currencies_implied = self.data_currencies_eur.loc[:, currency_implied].tolist()
                data_all_currencies_implied_base = self.data_currencies_eur.loc[:, CurrencyBaseImplied.EUR003M.value].tolist()

            for values in range(rows):

                # Set the start date to start the computation
                start_current_date_index_loc = self.data_currencies_usd.index.get_loc(tmp_start_date_computations)
                start_current_date_index = pd.to_datetime(self.data_currencies_usd.index[start_current_date_index_loc],
                                                          format='%d-%m-%Y')
                # Take the previous dates
                previous_start_date_index = self.data_currencies_usd.index[start_current_date_index_loc - 1]
                previous_start_date_index_loc = self.data_currencies_usd.index.get_loc(previous_start_date_index)

                previous_start_four_date_index = self.data_currencies_usd.index[previous_start_date_index_loc - 3]
                previous_start_four_date_loc = self.data_currencies_usd.index.get_loc(previous_start_four_date_index)

                # Do the averages
                # We use nanmean because we do average with nan and integers values sometimes
                average_implied = np.nanmean(data_all_currencies_implied[previous_start_four_date_loc:previous_start_date_index_loc+1])
                average_index = np.nanmean(data_all_currencies_implied_base[previous_start_four_date_loc:previous_start_date_index_loc+1])

                # Depending on the carry type, if it is real, we take off the inflation, otherwise, we don't
                if carry_type.lower() == 'real':
                    carry_tmp = ((average_implied - average_index) / 100) - inflation_differential[CurrencySpot.Inflation_Differential.value + currency_spot].loc[start_current_date_index]/100
                else:
                    carry_tmp = ((average_implied - average_index) / 100)

                # If one of the average don't have a nan, we can add the calculation to the list, otherwise, we perform
                # another calculation in the else statement
                if not np.isnan(carry_tmp):
                    carry.append(carry_tmp)

                else:

                    previous_start_date_loc = self.data_currencies_usd.index[start_current_date_index_loc - 1]
                    previous_start_date_index = self.data_currencies_usd.index.get_loc(previous_start_date_loc)

                    previous_eleven_start_date_loc = self.data_currencies_usd.index[start_current_date_index_loc - 11]
                    previous_eleven_start_date_index = self.data_currencies_usd.index.get_loc(previous_eleven_start_date_loc)

                    numerator = data_all_currencies_carry[previous_start_date_index] / data_all_currencies_carry[previous_eleven_start_date_index]
                    denominator = data_all_currencies_spot[previous_start_date_index] / data_all_currencies_spot[previous_eleven_start_date_index]

                    if carry_type.lower() == 'real':
                        carry.append((((numerator / denominator) ** (52/10))-1) - inflation_differential[CurrencySpot.Inflation_Differential.value + currency_spot].loc[start_current_date_index]/100)
                    else:
                        carry.append((((numerator / denominator) ** (52/10))-1))

                # Error handling when we reach the end of the dates range
                try:
                    tmp_start_date_computations = self.data_currencies_usd.index[start_current_date_index_loc + 1]
                except IndexError:
                    tmp_start_date_computations = self.data_currencies_usd.index[start_current_date_index_loc]

            self.carry_currencies[CurrencySpot.Carry.value + currency_spot] = carry

        self.carry_currencies = self.carry_currencies.set_index(self.dates_origin_index).apply(lambda x: x * 100)

        return self.carry_currencies

    def compute_trend(self, trend_ind, short_term, long_term):

        if trend_ind.lower() == 'total return':
            currencies = constants.CURRENCIES_CARRY
        else:
            currencies = constants.CURRENCIES_SPOT

        # Loop through each date
        for currency, currency_name_col in zip(currencies, constants.CURRENCIES_SPOT):
            if currency in self.data_currencies_usd.columns:
                trend_short_tmp = self.data_currencies_usd.loc[:, currency].rolling(short_term).mean()
                trend_long_tmp = self.data_currencies_usd.loc[:, currency].rolling(long_term).mean()
            else:
                trend_short_tmp = self.data_currencies_eur.loc[:, currency].rolling(short_term).mean()
                trend_long_tmp = self.data_currencies_eur.loc[:, currency].rolling(long_term).mean()

            # We set 10 digits because due to Python precision there are small dusts at the end of some numbers
            # and they set 0 as negative result (eg: date 16/02/2004: -0.000%)
            self.trend_currencies[CurrencySpot.Trend.name + currency_name_col] = \
                (round((trend_short_tmp / trend_long_tmp), 10) - 1) * 100

        # Take the previous date compared to self.date_computations because of rolling
        # start_date_loc = self.data_currencies_usd.index.get_loc(self.start_date_calculations)
        # previous_start_date = self.data_currencies_usd.index[start_date_loc - 1]
        self.trend_currencies = self.trend_currencies.shift(1)
        self.trend_currencies = self.trend_currencies[self.start_date_calculations:]

        # self.trend_currencies = self.trend_currencies[previous_start_date:].iloc[:-1]
        # self.trend_currencies = self.trend_currencies.set_index(self.dates_index)
        self.trend_currencies.to_csv("trend.csv")
        return self.trend_currencies

    def combo_computations(self, cut_off, incl_shorts, cut_off_s, threshold_for_closing):

        tmp_start_date_computations = self.start_date_calculations
        rows = self.data_currencies_usd[tmp_start_date_computations:].shape[0]

        for currency_spot in constants.CURRENCIES_SPOT:
            # Set the combo to zero as first value
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

        # Set the index
        self.combo_currencies = self.combo_currencies.set_index(self.dates_index)

        return self.combo_currencies

    def return_ex_costs_computations(self):

        for currency_carry, currency_spot in zip(constants.CURRENCIES_CARRY, constants.CURRENCIES_SPOT):

            first_returns = [100]

            tmp_start_computations_loc = self.data_currencies_usd.index.get_loc(pd.to_datetime(self.start_date_calculations)) - 1
            tmp_start_computations = self.data_currencies_usd.index[tmp_start_computations_loc]

            if currency_carry in self.data_currencies_usd.columns:
                return_division_tmp = (self.data_currencies_usd.loc[tmp_start_computations:, currency_carry] /
                                       self.data_currencies_usd.loc[tmp_start_computations:, currency_carry].shift(1))
            else:
                return_division_tmp = (self.data_currencies_eur.loc[tmp_start_computations:, currency_carry] /
                                       self.data_currencies_eur.loc[tmp_start_computations:, currency_carry].shift(1))

            combo = self.combo_currencies.loc[pd.to_datetime(self.start_date_calculations, format='%Y-%m-%d'):,
                                              CurrencySpot.Combo.name + currency_spot].tolist()

            return_division_tmp = return_division_tmp.iloc[1:].tolist()
            # return_tmp = return_division_tmp.tolist()

            # d = self.data_currencies_usd.index[18792:].tolist()
            # ret = pd.read_csv(r'C:\Users\AJ89720\PycharmProjects\assetallocation_arp\assetallocation_arp\models\effect\returns_mxn.csv')
            # ret = ret['Returns'].tolist()

            origin_returns = []
            for values in range(len(return_division_tmp)):
                # print(d[values], round(first_returns[values] * return_division_tmp[values] ** combo[values], 12), round(ret[values],12), round(ret[values],12) - round(first_returns[values] * return_division_tmp[values] ** combo[values], 12))

                first_returns.append(round(first_returns[values] * return_division_tmp[values] ** combo[values], 12))
                # origin_returns.append(round(ret[values], 12))

            self.return_ex_costs[CurrencySpot.Return_Ex_Costs.name + currency_spot] = first_returns
            # pd.DataFrame(first_returns[1:]).to_csv('brl_returns_ex_costs_results')
            #POUR LES TESTS ON UTILISE LES NUMPY ARRAY ET ON  COMPARE LES DEUX ARRAYS SI TRUE ON EST OKAY
            # o = np.array(origin_returns)
            # f = np.array(first_returns[1:])
            # print("%s IS EQUAL: %s" % (currency_spot, np.allclose(o, f)))
            # pd.DataFrame(first_returns).to_csv("returns_ex_costs_new_{}.csv".format(currency_spot))

        # Set the index with dates by taking into account the 100
        self.return_ex_costs = self.return_ex_costs.set_index(self.dates_index)

        return self.return_ex_costs

    def return_incl_costs_computations(self):

        returns_division_tmp = self.return_ex_costs / self.return_ex_costs.shift(1)

        returns_division_tmp = returns_division_tmp.iloc[1:]

        combo_substraction_tmp = abs(self.combo_currencies - self.combo_currencies.shift(1)).iloc[1:]

        currency_ex_costs = returns_division_tmp.columns.values.tolist()
        combo_names = self.combo_currencies.columns.tolist()

        for name, combo_name in zip(currency_ex_costs, combo_names):
            return_incl_costs = [100]
            return_tmp = returns_division_tmp[name].tolist()
            combo_values_tmp = combo_substraction_tmp[combo_name].tolist()

            multiplier_combo = [(1 - self.bid_ask / 20000) ** value for value in combo_values_tmp]

            for value in range(len(return_tmp)):
                return_incl_costs.append(return_incl_costs[value] * return_tmp[value] * multiplier_combo[value])

            self.return_incl_costs[name.replace(CurrencySpot.Return_Ex_Costs.name,
                                                CurrencySpot.Return_Incl_Costs.name)] = return_incl_costs

        self.return_incl_costs = self.return_incl_costs.set_index(self.dates_index)

        return self.return_incl_costs

    def spot_ex_costs_computations(self):

        start_date_loc = self.data_currencies_usd.index.get_loc(self.start_date_calculations) - 1
        tmp_start_date = self.data_currencies_usd.index[start_date_loc]

        # loop to get through each currency
        for currency in constants.CURRENCIES_SPOT:
            # Reset the Spot list for the next currency
            spot = [100]  # the Spot is set 100
            if currency in self.data_currencies_usd.columns:
                spot_division_tmp = (self.data_currencies_usd.loc[tmp_start_date:, currency] /
                                     self.data_currencies_usd.loc[tmp_start_date:, currency].shift(1))
            else:
                spot_division_tmp = (self.data_currencies_eur.loc[tmp_start_date:, currency] /
                                     self.data_currencies_eur.loc[tmp_start_date:, currency].shift(1))

            combo = self.combo_currencies.loc[self.start_date_calculations:, CurrencySpot.Combo.name + currency].tolist()
            # Remove the first nan due to the shift(1) and convert the spot_division_tmp into a list
            spot_division_tmp = spot_division_tmp.iloc[1:].tolist()

            # Compute with the previous Spot
            for value in range(len(spot_division_tmp)):
                spot.append(spot[value] * spot_division_tmp[value] ** combo[value])

            # Store all the spot for each currency
            self.spot_ex_costs[CurrencySpot.Spot_Ex_Costs.name + currency] = spot

        # Set the dates to the index of self.spot_ex_costs
        self.spot_ex_costs = self.spot_ex_costs.set_index(self.dates_index)

        return self.spot_ex_costs

    def spot_incl_computations(self):

        spot_division_tmp = self.spot_ex_costs / self.spot_ex_costs.shift(1)

        spot_division_tmp = spot_division_tmp.iloc[1:]

        combo_substraction_tmp = abs(self.combo_currencies - self.combo_currencies.shift(1)).iloc[1:]

        currency_incl_costs = spot_division_tmp.columns.values.tolist()
        combo_names = self.combo_currencies.columns.tolist()

        for name, combo_name in zip(currency_incl_costs, combo_names):
            spot_incl_costs = [100]
            spot_tmp = spot_division_tmp[name].tolist()
            combo_values_tmp = combo_substraction_tmp[combo_name].tolist()

            multiplier_combo = [(1 - self.bid_ask / 20000) ** value for value in combo_values_tmp]

            for value in range(len(spot_tmp)):
                spot_incl_costs.append(spot_incl_costs[value] * spot_tmp[value] * multiplier_combo[value])

            self.spot_incl_costs[name.replace(CurrencySpot.Return_Ex_Costs.name,
                                              CurrencySpot.Return_Incl_Costs.name)] = spot_incl_costs

        self.spot_incl_costs = self.spot_incl_costs.set_index(self.dates_index)

        return self.spot_incl_costs