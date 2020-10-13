"""
Created on 12/05/2020
@author: AJ89720
"""
import warnings
import pandas as pd
import numpy as np

from data_etl.inputs_effect.process_data_effect import ProcessDataEffect
from assetallocation_arp.common_libraries.names_columns_calculations import CurrencySpot
from assetallocation_arp.common_libraries.names_currencies_implied import CurrencyBaseImplied
from data_etl.outputs_effect.write_logs_computations_effect import write_logs_effect


"""
    Class to compute the different calculations for usd and eur currencies
"""


class ComputeCurrencies(ProcessDataEffect):

    def __init__(self, asset_inputs, frequency_mat, end_date_mat, signal_day_mat, all_data, bid_ask_spread=10):
        super().__init__(asset_inputs, frequency_mat, end_date_mat, signal_day_mat, all_data)

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
        write_logs_effect("Computing carry...", "logs_carry")
        for currency_spot, currency_implied, currency_carry in \
                zip(self.all_currencies_spot, self.all_currencies_3M_implied, self.all_currencies_carry):

            tmp_start_date_computations = self.start_date_calculations

            rows = self.data_currencies_usd[tmp_start_date_computations:].shape[0]

            carry = []

            if currency_spot in self.data_currencies_usd.columns:
                data_all_currencies_spot = self.spot_usd.loc[:, currency_spot].tolist()
                data_all_currencies_carry = self.carry_usd.loc[:, currency_carry].tolist()
                data_all_currencies_implied = self.three_month_implied_usd.loc[:, currency_implied].tolist()
                data_all_currencies_implied_base = self.base_implied_usd.loc[:, CurrencyBaseImplied.US0003M.value].tolist()
            else:
                data_all_currencies_spot = self.spot_eur.loc[:, currency_spot].tolist()
                data_all_currencies_carry = self.carry_eur.loc[:, currency_carry].tolist()
                data_all_currencies_implied = self.three_month_implied_eur.loc[:, currency_implied].tolist()
                data_all_currencies_implied_base = self.base_implied_eur.loc[:, CurrencyBaseImplied.EUR003M.value].tolist()

            for values in range(rows):

                # Set the start date to start the computation
                start_current_date_index_loc = self.data_currencies_usd.index.get_loc(tmp_start_date_computations)
                start_current_date_index = self.data_currencies_usd.index[start_current_date_index_loc]

                # Take the previous dates
                previous_start_date_index = self.data_currencies_usd.index[start_current_date_index_loc - 1]
                previous_start_date_index_loc = self.data_currencies_usd.index.get_loc(previous_start_date_index)

                previous_start_four_date_index = self.data_currencies_usd.index[previous_start_date_index_loc - 3]
                previous_start_four_date_loc = self.data_currencies_usd.index.get_loc(previous_start_four_date_index)

                # Do the averages and avoid RuntimeWarning: Mean of empty slice message on the Python console
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=RuntimeWarning)
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
        write_logs_effect("Computing trend...", "logs_trend")
        if trend_ind.lower() == 'total return':
            currencies = self.all_currencies_carry
        else:
            currencies = self.all_currencies_spot

        # Loop through each date
        for currency, currency_name_col in zip(currencies, self.all_currencies_spot):
            if currency in self.data_currencies_usd.columns:
                trend_short_tmp = self.data_currencies_usd.loc[:, currency].rolling(short_term).mean()
                trend_long_tmp = self.data_currencies_usd.loc[:, currency].rolling(long_term).mean()
            else:
                trend_short_tmp = self.data_currencies_eur.loc[:, currency].rolling(short_term).mean()
                trend_long_tmp = self.data_currencies_eur.loc[:, currency].rolling(long_term).mean()

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
        write_logs_effect("Computing combo...", "logs_combo")
        tmp_start_date_computations = self.start_date_calculations
        rows = self.data_currencies_usd[tmp_start_date_computations:].shape[0]

        for currency_spot in self.all_currencies_spot:
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
        write_logs_effect("Computing return exclude costs...", "logs_ret_ex")
        for currency_carry, currency_spot in zip(self.all_currencies_carry, self.all_currencies_spot):

            first_returns = [100]

            tmp_start_computations_loc = self.data_currencies_usd.index.get_loc(self.start_date_calculations) - 1
            tmp_start_computations = self.data_currencies_usd.index[tmp_start_computations_loc]

            if currency_carry in self.data_currencies_usd.columns:
                carry_division_tmp = (self.carry_usd.loc[tmp_start_computations:, currency_carry] /
                                      self.carry_usd.loc[tmp_start_computations:, currency_carry].shift(1))
                bool_base_currency = self.weight_percentage_usd[currency_spot].item() / 100
            else:
                carry_division_tmp = (self.carry_eur.loc[tmp_start_computations:, currency_carry] /
                                      self.carry_eur.loc[tmp_start_computations:, currency_carry].shift(1))
                bool_base_currency = 1 - self.weight_percentage_eur[currency_spot].item() / 100

            # EURUSDCR Currency
            eur_usd_cr_tmp = (self.eur_usd_cr.loc[tmp_start_computations:] / self.eur_usd_cr.loc[tmp_start_computations:].shift(1)).iloc[1:].tolist()

            combo = self.combo_currencies.loc[self.start_date_calculations:, CurrencySpot.Combo.value + currency_spot].tolist()

            carry_division_tmp = carry_division_tmp.iloc[1:].tolist()

            for values in range(len(carry_division_tmp)):
                try:
                    first_returns.append(round(first_returns[values] *
                                         carry_division_tmp[values] ** combo[values] / eur_usd_cr_tmp[values] ** bool_base_currency, 12))
                except ZeroDivisionError:
                    first_returns.append(0)
            self.return_ex_costs[CurrencySpot.Return_Ex_Costs.value + currency_spot] = first_returns

        # Set the index with dates by taking into account the 100
        self.return_ex_costs = self.return_ex_costs.set_index(self.dates_index)

        return self.return_ex_costs

    def compute_return_incl_costs(self):
        """
        Function calculating the return included costs for usd and eur currencies
        :return: a dataFrame self.return_incl_costs of return included costs for usd and eur currencies
        """
        write_logs_effect("Computing return include costs...", "logs_ret_inc")
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
                try:
                    return_incl_costs.append(return_incl_costs[value] * return_tmp[value] * multiplier_combo[value])
                except ZeroDivisionError:
                    return_incl_costs.append(0)

            self.return_incl_costs[name.replace(CurrencySpot.Return_Ex_Costs.value,
                                                CurrencySpot.Return_Incl_Costs.value)] = return_incl_costs

        self.return_incl_costs = self.return_incl_costs.set_index(self.dates_index)

        return self.return_incl_costs

    def compute_spot_ex_costs(self):
        """
        Function calculating the spot excluded costs
        :return: a dataFrame self.spot_ex_costs of spot excluded costs data for usd and eur currencies
        """
        write_logs_effect("Computing spot exclude costs...", "logs_spot_ex")
        start_date_loc = self.data_currencies_usd.index.get_loc(self.start_date_calculations) - 1
        tmp_start_date = self.data_currencies_usd.index[start_date_loc]

        # Loop to get through each currency
        for currency in self.all_currencies_spot:
            # Reset the Spot list for the next currency
            spot = [100]  # The Spot is set 100
            if currency in self.data_currencies_usd.columns:

                spot_division_tmp = (self.spot_usd.loc[tmp_start_date:, currency] /
                                     self.spot_usd.loc[tmp_start_date:, currency].shift(1))
            else:
                spot_division_tmp = (self.spot_eur.loc[tmp_start_date:, currency] /
                                     self.spot_eur.loc[tmp_start_date:, currency].shift(1))

            combo = self.combo_currencies.loc[self.start_date_calculations:, CurrencySpot.Combo.value + currency].tolist()

            # Remove the first nan due to the shift(1) and convert the spot_division_tmp into a list
            spot_division_tmp = spot_division_tmp.iloc[1:].tolist()

            # Compute with the previous Spot
            for value in range(len(spot_division_tmp)):
                try:
                    spot.append(spot[value] * spot_division_tmp[value] ** combo[value])
                except ZeroDivisionError:
                    spot.append(0)

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
        write_logs_effect("Computing spot include costs...", "logs_spot_inc")
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
                try:
                    spot_incl_costs.append(spot_incl_costs[value] * spot_tmp[value] * multiplier_combo[value])
                except ZeroDivisionError:
                    spot_incl_costs.append(0)

            self.spot_incl_costs[name.replace(CurrencySpot.Spot_Ex_Costs.value,
                                              CurrencySpot.Spot_Incl_Costs.value)] = spot_incl_costs

        self.spot_incl_costs = self.spot_incl_costs.set_index(self.dates_index)

        return self.spot_incl_costs

    def run_compute_currencies(self, carry_inputs, trend_inputs, combo_inputs):
        """
        Function calling all the functions above
        :param carry_inputs: carry_inputs inputs from the dashboard
        :param trend_inputs: trend_inputs inputs from the dashboard
        :param combo_inputs: combo_inputs inputs from the dashboard
        :return: a dictionary
        """
        carry = self.compute_carry(carry_type=carry_inputs['type'], inflation_differential=carry_inputs['inflation'])

        trend = self.compute_trend(trend_ind=trend_inputs['trend'], short_term=trend_inputs['short_term'],
                                   long_term=trend_inputs['long_term'])

        combo = self.compute_combo(cut_off=combo_inputs['cut_off'], incl_shorts=combo_inputs['incl_shorts'],
                                   cut_off_s=combo_inputs['cut_off_s'],
                                   threshold_for_closing=combo_inputs['threshold'])

        return_ex = self.compute_return_ex_costs()
        return_incl = self.compute_return_incl_costs()

        spot_ex = self.compute_spot_ex_costs()
        spot_incl = self.compute_spot_incl_costs()

        currencies_calculations = {'carry_curr': carry, 'trend_curr': trend, 'combo_curr': combo,
                                   'return_excl_curr': return_ex, 'return_incl_curr': return_incl,
                                   'spot_excl_curr': spot_ex, 'spot_incl_curr': spot_incl}

        return currencies_calculations
