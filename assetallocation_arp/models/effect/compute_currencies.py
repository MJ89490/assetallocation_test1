"""
Created on 12/05/2020
@author: AJ89720
"""

from data_etl.inputs_effect.import_process_data_effect import ProcessDataEffect
from assetallocation_arp.common_libraries.names_columns_calculations import CurrencySpot
import common_libraries.names_all_currencies as constants
from common_libraries.names_currencies_implied import CurrencyBaseImplied
import pandas as pd
import numpy as np

"""
    Class to compute the different calculations for usd and eur currencies
"""


class ComputeCurrencies(ProcessDataEffect):

    def __init__(self, start_date_calculations='2000-01-11', bid_ask_spread=10):
        super().__init__(start_date_calculations=start_date_calculations)

        self.carry_currencies = pd.DataFrame()
        self.trend_currencies = pd.DataFrame()
        self.spot_ex_costs = pd.DataFrame()
        self.spot_incl_costs = pd.DataFrame()
        self.return_ex_costs = pd.DataFrame()
        self.return_incl_costs = pd.DataFrame()
        self.combo_currencies = pd.DataFrame()

        self.bid_ask_spread = bid_ask_spread

    @property
    def bid_ask_spread(self):
        return self._bid_ask_spread

    @bid_ask_spread.setter
    def bid_ask_spread(self, value):
        self._bid_ask_spread = value

    def compute_carry(self, carry_type, inflation_differential):
        """
        Function calculating the carry for usd and eur currencies
        :param carry_type: string value depending on the user input: Real or Nominal
        :param inflation_differential: dataFrame with inflation differential data
        :return: a dataFrame self.carry_currencies of carry data for usd and eur currencies
        """

        for currency_spot, currency_implied, currency_carry in \
                zip(constants.CURRENCIES_SPOT, constants.CURRENCIES_IMPLIED, constants.CURRENCIES_CARRY):

            tmp_start_date_computations = self.start_date_calculations

            rows = self.data_currencies_usd[tmp_start_date_computations:].shape[0]

            carry = []

            if currency_spot in self.data_currencies_usd.columns:
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
        """
        Function calculating the trend for usd and eur currencies
        :param trend_ind: string user input: Spot or Total Return
        :param short_term: integer user input required to compute the short moving average
        :param long_term: integer user input required to compute the long moving average
        :return: a dataFrame self.trend_currencies of trend data for usd and eur currencies
        """

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

                self.data_currencies_eur.loc[:, currency].to_csv('spot_pln.csv')

            # We set 10 digits because due to Python precision there are small dusts at the end of some numbers
            # and they set 0 as negative result (eg: date 16/02/2004: -0.000%)
            self.trend_currencies[CurrencySpot.Trend.value + currency_name_col] = \
                (round((trend_short_tmp / trend_long_tmp), 10) - 1) * 100

        # Take the previous date compared to self.date_computations because of rolling
        self.trend_currencies = self.trend_currencies.shift(1)
        self.trend_currencies = self.trend_currencies[self.start_date_calculations:]

        return self.trend_currencies

    def compute_combo(self, cut_off, incl_shorts, cut_off_s, threshold_for_closing):
        """
        Function calculating the combo for usd and eur currencies
        :param cut_off: integer user input
        :param incl_shorts: string user input (Yes or No)
        :param cut_off_s: integer user input
        :param threshold_for_closing: integer user input
        :return: a dataFrame self.combo_currencies of combo data for usd and eur currencies
        """

        tmp_start_date_computations = self.start_date_calculations
        rows = self.data_currencies_usd[tmp_start_date_computations:].shape[0]

        for currency_spot in constants.CURRENCIES_SPOT:
            # Set the combo to zero as first value
            combo = [0]
            trend = self.trend_currencies.loc[tmp_start_date_computations:, CurrencySpot.Trend.value + currency_spot].tolist()
            carry = self.carry_currencies.loc[tmp_start_date_computations:, CurrencySpot.Carry.value + currency_spot].tolist()

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

            self.combo_currencies[CurrencySpot.Combo.value + currency_spot] = combo

        # Set the index
        self.combo_currencies = self.combo_currencies.set_index(self.dates_index)

        return self.combo_currencies

    def compute_return_ex_costs(self):
        """
        Function calculating return exclude costs for usd and eur currencies
        :return: a dataFrame self.return_ex_costs of return exclude costs data for usd and eur currencies
        """

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
                                              CurrencySpot.Combo.value + currency_spot].tolist()

            return_division_tmp = return_division_tmp.iloc[1:].tolist()

            for values in range(len(return_division_tmp)):
                first_returns.append(round(first_returns[values] * return_division_tmp[values] ** combo[values], 12))

            self.return_ex_costs[CurrencySpot.Return_Ex_Costs.value + currency_spot] = first_returns

        # Set the index with dates by taking into account the 100
        self.return_ex_costs = self.return_ex_costs.set_index(self.dates_index)

        return self.return_ex_costs

    def compute_return_incl_costs(self):
        """
        Function calculating the return included costs for usd and eur currencies
        :return: a dataFrame self.return_incl_costs of return included costs for usd and eur currencies
        """

        returns_division_tmp = self.return_ex_costs / self.return_ex_costs.shift(1)

        returns_division_tmp = returns_division_tmp.iloc[1:]

        combo_substraction_tmp = abs(self.combo_currencies - self.combo_currencies.shift(1)).iloc[1:]

        currency_ex_costs = returns_division_tmp.columns.values.tolist()
        combo_names = self.combo_currencies.columns.tolist()

        for name, combo_name in zip(currency_ex_costs, combo_names):
            return_incl_costs = [100]
            return_tmp = returns_division_tmp[name].tolist()
            combo_values_tmp = combo_substraction_tmp[combo_name].tolist()

            multiplier_combo = [(1 - self.bid_ask_spread / 20000) ** value for value in combo_values_tmp]

            for value in range(len(return_tmp)):
                return_incl_costs.append(return_incl_costs[value] * return_tmp[value] * multiplier_combo[value])

            self.return_incl_costs[name.replace(CurrencySpot.Return_Ex_Costs.value,
                                                CurrencySpot.Return_Incl_Costs.value)] = return_incl_costs

        self.return_incl_costs = self.return_incl_costs.set_index(self.dates_index)

        return self.return_incl_costs

    def compute_spot_ex_costs(self):
        """
        Function calculating the spot excluded costs
        :return: a dataFrame self.spot_ex_costs of spot excluded costs data for usd and eur currencies
        """

        start_date_loc = self.data_currencies_usd.index.get_loc(self.start_date_calculations) - 1
        tmp_start_date = self.data_currencies_usd.index[start_date_loc]

        # Loop to get through each currency
        for currency in constants.CURRENCIES_SPOT:
            # Reset the Spot list for the next currency
            spot = [100]  # The Spot is set 100
            if currency in self.data_currencies_usd.columns:

                spot_division_tmp = (self.data_currencies_usd.loc[tmp_start_date:, currency] /
                                     self.data_currencies_usd.loc[tmp_start_date:, currency].shift(1))
            else:
                spot_division_tmp = (self.data_currencies_eur.loc[tmp_start_date:, currency] /
                                     self.data_currencies_eur.loc[tmp_start_date:, currency].shift(1))

            combo = self.combo_currencies.loc[self.start_date_calculations:, CurrencySpot.Combo.value + currency].tolist()

            # Remove the first nan due to the shift(1) and convert the spot_division_tmp into a list
            spot_division_tmp = spot_division_tmp.iloc[1:].tolist()

            # Compute with the previous Spot
            for value in range(len(spot_division_tmp)):
                spot.append(spot[value] * spot_division_tmp[value] ** combo[value])

            # Store all the spot for each currency
            self.spot_ex_costs[CurrencySpot.Spot_Ex_Costs.value + currency] = spot

        # Set the dates to the index of self.spot_ex_costs
        self.spot_ex_costs = self.spot_ex_costs.set_index(self.dates_index)

        return self.spot_ex_costs

    def compute_spot_incl_costs(self):
        """
        Function calculating spot included costs for usd and eur currencies
        :return: a dataFrame self.spot_incl_costs of spot included costs for usd and eur currencies
        """

        spot_division_tmp = self.spot_ex_costs / self.spot_ex_costs.shift(1)

        spot_division_tmp = spot_division_tmp.iloc[1:]

        combo_substraction_tmp = abs(self.combo_currencies - self.combo_currencies.shift(1)).iloc[1:]

        currency_incl_costs = spot_division_tmp.columns.values.tolist()
        combo_names = self.combo_currencies.columns.tolist()

        for name, combo_name in zip(currency_incl_costs, combo_names):
            spot_incl_costs = [100]
            spot_tmp = spot_division_tmp[name].tolist()
            combo_values_tmp = combo_substraction_tmp[combo_name].tolist()

            multiplier_combo = [(1 - self.bid_ask_spread / 20000) ** value for value in combo_values_tmp]

            for value in range(len(spot_tmp)):
                spot_incl_costs.append(spot_incl_costs[value] * spot_tmp[value] * multiplier_combo[value])

            self.spot_incl_costs[name.replace(CurrencySpot.Spot_Ex_Costs.value,
                                              CurrencySpot.Spot_Incl_Costs.value)] = spot_incl_costs

        self.spot_incl_costs = self.spot_incl_costs.set_index(self.dates_index)

        return self.spot_incl_costs
