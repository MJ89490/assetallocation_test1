from configparser import ConfigParser
import os
import json
import pandas as pd
import statistics as stats
import math
import numpy as np


class ComputeAggregateCurrencies:

    def __init__(self, window, start_date_calculations, weight, dates_index):
        self.start_date_calc = start_date_calculations
        self.dates_index = dates_index
        self.window = window
        self.weight = weight

    @property
    def window(self):
        return self._window

    @window.setter
    def window(self, value):
        self._window = value

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        self._weight = value

    def compute_inverse_volatility(self, spot_data):

        inverse_volatilities = pd.DataFrame()

        for currency_spot in spot_data.columns:

            tmp_start_date_computations = self.start_date_calc
            rows = spot_data[tmp_start_date_computations:].shape[0]

            spot_tmp = spot_data.loc[:, currency_spot]
            volatilities = []

            for value in range(rows):
                # Set the start date to start the computation
                start_current_date_index_loc = spot_data.index.get_loc(tmp_start_date_computations)
                start_current_date_index = spot_data.index[start_current_date_index_loc]

                # Take previous date depending on the size of the window
                previous_start_date_index = spot_data.index[start_current_date_index_loc - self.window]
                previous_start_date_index_loc = spot_data.index.get_loc(previous_start_date_index)

                # Take the previous values depending on the size of the window
                values_window = spot_tmp[previous_start_date_index:start_current_date_index]

                values_rolling_window = values_window / values_window.shift(1)

                # Compute the standard deviation and the inverse volatility per currency
                try:
                    volatility = 1 / (math.sqrt(52) * stats.stdev(values_rolling_window.iloc[1:]))
                except ZeroDivisionError:
                    volatility = 0

                # Add the standard deviation results into a list
                volatilities.append(volatility)

                # Error handling when we reach the end of the dates range
                try:
                    tmp_start_date_computations = spot_data.index[start_current_date_index_loc + 1]
                except IndexError:
                    tmp_start_date_computations = spot_data.index[start_current_date_index_loc]

            # Add volatilities into a common dataFrame
            inverse_volatilities['Inverse_Volatility_' + currency_spot] = volatilities

        inverse_volatilities = inverse_volatilities.set_index(self.dates_index)

        return inverse_volatilities

    def compute_excl_signals_total_return(self, carry_origin):
        """
        Function computing Excl signals (total return) dividing the current value by the start date value
        :param carry_origin: carry data from Bloomberg for all currencies
        :return: dataFrame of Excl signals (total return)
        """
        return (carry_origin.loc[self.start_date_calc:] / carry_origin.loc[self.start_date_calc]).apply(lambda x: x * 100)

    def compute_excl_signals_spot_return(self, spot_origin):
        """
        Function computing Excl signals (spot return) dividing the current value by the start date value
        :param spot_origin: spot data from Blommberg for all currencies
        :return: dataFrame of Excl signals (spot return)
        """

        return (spot_origin.loc[self.start_date_calc:] / spot_origin.loc[self.start_date_calc]).apply(lambda x: x * 100)

    def compute_aggregate_total_incl_signals(self, returns_incl_costs):

        first_total_signals = [100]
        total_incl_signals = pd.DataFrame()

        if self.weight == '1/N':
            average_incl_signals = (returns_incl_costs.loc[self.start_date_calc:] / returns_incl_costs.loc[self.start_date_calc:].shift(1)).mean(axis=1).iloc[1:].tolist()
            for value in range(len(average_incl_signals)):
                first_total_signals.append(first_total_signals[value] * average_incl_signals[value])

            total_incl_signals['Total_Incl_Signals'] = first_total_signals

        total_incl_signals = total_incl_signals.set_index(self.dates_index)

        return total_incl_signals

    def compute_aggregate_total_excl_signals(self, returns_excl_costs):

        first_total_signals = [100]
        total_excl_signals = pd.DataFrame()

        if self.weight == '1/N':
            average_excl_signals = (returns_excl_costs.loc[self.start_date_calc:] / returns_excl_costs.loc[self.start_date_calc:].shift(1)).mean(axis=1).iloc[1:].tolist()
            for value in range(len(average_excl_signals)):
                first_total_signals.append(first_total_signals[value] * average_excl_signals[value])

            total_excl_signals['Total_Excl_Signals'] = first_total_signals

        total_excl_signals = total_excl_signals.set_index(self.dates_index)

        return total_excl_signals

    def compute_aggregate_spot_incl_signals(self, spot_incl_costs):

        first_spot_incl_signals = [100]
        spot_incl_signals = pd.DataFrame()

        if self.weight == '1/N':
            average_spot_incl_signals = (spot_incl_costs.loc[self.start_date_calc:] / spot_incl_costs.loc[self.start_date_calc:].shift(1)).mean(axis=1).iloc[1:].tolist()
            for value in range(len(average_spot_incl_signals)):
                first_spot_incl_signals.append(first_spot_incl_signals[value] * average_spot_incl_signals[value])

            spot_incl_signals['Spot_Incl_Signals'] = first_spot_incl_signals

        spot_incl_signals = spot_incl_signals.set_index(self.dates_index)

        return spot_incl_signals

    def compute_aggregate_spot_excl_signals(self, spot_excl_costs):

        first_spot_excl_signals = [100]
        spot_excl_signals = pd.DataFrame()

        if self.weight == '1/N':
            average_spot_excl_signals = (spot_excl_costs.loc[self.start_date_calc:] / spot_excl_costs.loc[self.start_date_calc:].shift(1)).mean(axis=1).iloc[1:].tolist()
            for value in range(len(average_spot_excl_signals)):
                first_spot_excl_signals.append(first_spot_excl_signals[value] * average_spot_excl_signals[value])

            spot_excl_signals['Spot_Excl_Signals'] = first_spot_excl_signals

        spot_excl_signals = spot_excl_signals.set_index(self.dates_index)

        return spot_excl_signals

    @staticmethod
    def compute_log_returns_excl_costs(returns_ex_costs):

        return np.log((returns_ex_costs / returns_ex_costs.shift(1)).iloc[1:])

    def compute_weighted_performance(self, log_returns_excl, combo_curr):

        # Instantiate ConfigParser
        config = ConfigParser()
        # Parse existing file
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'matr_weights_effect.ini'))
        config.read(path)
        weights = json.loads(config.get('weighted_performance', 'weights'))
        start_date_perf = config.get('start_date_weighted_performance', 'start_date_weighted_perf')
        start_date_weighted_performance = pd.to_datetime(start_date_perf, format='%d-%m-%Y')

        index_weighted_performance = pd.DataFrame(self.dates_index, columns=['Dates_Weighted_Performance'])
        index_weighted = index_weighted_performance[index_weighted_performance.Dates_Weighted_Performance >= start_date_weighted_performance]

        log_returns_excl = log_returns_excl.loc[start_date_weighted_performance:]
        combo = combo_curr.loc[start_date_weighted_performance:]

        sum_prod = []
        weighted_perf = []

        for values_combo, values_log in zip(combo.values, log_returns_excl.values):
            tmp = []
            for value_combo, value_log in zip(values_combo, values_log):
                tmp.append(value_combo * value_log)
            sum_prod.append(sum(tmp))

        for value_weight in range(len(weights)):
            weighted_perf.append(sum_prod[value_weight] * float(list(weights.values())[value_weight]))

        return pd.DataFrame(weighted_perf, columns=['Weighted_Performance'], index=index_weighted.Dates_Weighted_Performance.tolist())

    def run_aggregate_currencies(self, returns_incl_costs, spot_incl_costs, spot_origin, carry_origin, combo_curr):

        inverse_volatilies = self.compute_inverse_volatility(spot_data=spot_origin)

        excl_signals_total_return = self.compute_excl_signals_total_return(carry_origin=carry_origin)
        excl_signals_spot_return = self.compute_excl_signals_spot_return(spot_origin=spot_origin)

        log_returns_excl_costs = self.compute_log_returns_excl_costs(returns_ex_costs=excl_signals_total_return)
        weighted_performance = self.compute_weighted_performance(log_returns_excl=log_returns_excl_costs, combo_curr=combo_curr)

        aggregate_total_incl_signals = self.compute_aggregate_total_incl_signals(returns_incl_costs=returns_incl_costs)
        aggregate_total_excl_signals = self.compute_aggregate_total_excl_signals(returns_excl_costs=excl_signals_total_return)

        aggregate_spot_incl_signals = self.compute_aggregate_spot_incl_signals(spot_incl_costs=spot_incl_costs)
        aggregate_spot_excl_signals = self.compute_aggregate_spot_excl_signals(spot_excl_costs=excl_signals_spot_return)

        return {'agg_total_incl_signals': aggregate_total_incl_signals,
                'agg_total_excl_signals': aggregate_total_excl_signals,
                'agg_spot_incl_signals': aggregate_spot_incl_signals,
                'agg_spot_excl_signals': aggregate_spot_excl_signals,
                'weighted_performance': weighted_performance, 'log_returns_excl_costs': log_returns_excl_costs}
