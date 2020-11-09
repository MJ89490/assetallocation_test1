from assetallocation_arp.common_libraries.names_columns_calculations import CurrencyAggregate

import pandas as pd
import statistics as stats
import math
import numpy as np


class ComputeAggregateCurrencies:

    def __init__(self, window, start_date_calculations, weight, dates_index, prev_start_date_calc):
        self.start_date_calc = start_date_calculations
        self.dates_index = dates_index
        self.window = window
        self.weight = weight
        self.prev_start_date_calc = prev_start_date_calc

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
        """
        Function computing the inverse volatility if the weight is equal to 1/inverse_volatility
        :param spot_data: spot data from compute currencies class
        :return: a dataFrame with inverse volatility data
        """

        inverse_volatility = pd.DataFrame()

        for currency_spot in spot_data.columns:

            tmp_start_date_computations = self.start_date_calc
            rows = spot_data[tmp_start_date_computations:].shape[0]

            spot_tmp = spot_data.loc[:, currency_spot]
            volatility_values = []

            for value in range(rows):
                # Set the start date to start the computation
                start_current_date_index_loc = spot_data.index.get_loc(tmp_start_date_computations)
                start_current_date_index = spot_data.index[start_current_date_index_loc]

                # Take previous date depending on the size of the window
                previous_start_date_index = spot_data.index[start_current_date_index_loc - self.window]

                # Take the previous values depending on the size of the window
                values_window = spot_tmp[previous_start_date_index:start_current_date_index]

                values_rolling_window = values_window / values_window.shift(1)

                # Compute the standard deviation and the inverse volatility per currency
                try:
                    volatility = 1 / (math.sqrt(52) * stats.stdev(values_rolling_window.iloc[1:]))
                except ZeroDivisionError:
                    volatility = 0

                # Add the standard deviation results into a list
                volatility_values.append(volatility)

                # Error handling when we reach the end of the dates range
                try:
                    tmp_start_date_computations = spot_data.index[start_current_date_index_loc + 1]
                except IndexError:
                    tmp_start_date_computations = spot_data.index[start_current_date_index_loc]

            # Add volatility into a common dataFrame
            inverse_volatility[CurrencyAggregate.Inverse_Volatility.name + currency_spot] = volatility_values

        inverse_volatility = inverse_volatility.set_index(self.dates_index)

        return inverse_volatility

    def compute_excl_signals_total_return(self, carry_origin):
        """
        Function computing Excl signals (total return) dividing the current value by the start date value
        :param carry_origin: carry data from Bloomberg for all currencies
        :return: dataFrame of Excl signals (total return)
        """

        return (carry_origin.loc[self.prev_start_date_calc:] / carry_origin.loc[self.prev_start_date_calc]).apply(lambda x: x * 100)

    def compute_excl_signals_spot_return(self, spot_origin):
        """
        Function computing Excl signals (spot return) dividing the current value by the start date value
        :param spot_origin: spot data from Bloomberg for all currencies
        :return: dataFrame of Excl signals (spot return)
        """

        return (spot_origin.loc[self.prev_start_date_calc:] / spot_origin.loc[self.prev_start_date_calc]).apply(lambda x: x * 100)

    @staticmethod
    def compute_aggregate_inverse_volatility(returns_spot_values, inverse_volatility):
        """
        Function making the calculations for the aggregate functions below according to inverse volatility values
        This function is only called when the weight is equal to 1/inverse_volatility
        :param returns_spot_values: returns_incl_costs or spot_incl_costs values depending on the aggreate functions below
        :param inverse_volatility: inverse volatility values from compute_inverse_volatility
        :return: a list
        """
        inv_volatility_values = [100]
        counter = 0
        for values_returns, values_volatility in zip(returns_spot_values.values, inverse_volatility.values):
            tmp = []
            for value_returns, value_volatility in zip(values_returns, values_volatility):
                tmp.append(value_returns * value_volatility)
            sum_tmp_volatility = sum(values_volatility)
            inv_volatility_values.append(inv_volatility_values[counter] * (sum(tmp) / sum_tmp_volatility))
            counter += 1
        # inv_volatility_values.pop(0)
        return inv_volatility_values

    def compute_aggregate_total_incl_signals(self, returns_incl_costs, inverse_volatility):
        """
        Function computing the Total Incl Signals
        :param returns_incl_costs: values of returns_incl_costs
        :param inverse_volatility: values of inverse_volatility
        :return: a dataFrame with Total Incl Signals values
        """

        total_incl_signals_values = [100]

        if self.weight == '1/N':
            average_incl_signals = (returns_incl_costs / returns_incl_costs.shift(1)).mean(axis=1).iloc[1:].tolist()
            for value in range(len(average_incl_signals)):
                total_incl_signals_values.append(total_incl_signals_values[value] * average_incl_signals[value])
            # total_incl_signals_values.pop(0)
        else:
            returns_shift = (returns_incl_costs / returns_incl_costs.shift(1)).iloc[1:]
            total_incl_signals_values = self.compute_aggregate_inverse_volatility(returns_shift, inverse_volatility)

        return pd.DataFrame(total_incl_signals_values, columns=[CurrencyAggregate.Total_Incl_Signals.name], index=list(self.dates_index))

    def compute_aggregate_total_excl_signals(self, returns_excl_costs, inverse_volatility):
        """
        Function computing the Total Excl Signals
        :param returns_excl_costs: values of returns_excl_costs
        :param inverse_volatility: values of inverse_volatility
        :return: a dataFrame with Total Excl Signals values
        """

        total_excl_signals_values = [100]

        if self.weight == '1/N':
            average_excl_signals = (returns_excl_costs / returns_excl_costs.shift(1)).mean(axis=1).iloc[1:].tolist()
            for value in range(len(average_excl_signals)):
                total_excl_signals_values.append(total_excl_signals_values[value] * average_excl_signals[value])
            # total_excl_signals_values.pop(0)
        else:
            returns_shift = (returns_excl_costs / returns_excl_costs.shift(1)).iloc[1:]
            total_excl_signals_values = self.compute_aggregate_inverse_volatility(returns_shift, inverse_volatility)

        return pd.DataFrame(total_excl_signals_values, columns=[CurrencyAggregate.Total_Excl_Signals.name], index=list(self.dates_index))

    def compute_aggregate_spot_incl_signals(self, spot_incl_costs, inverse_volatility):
        """
        Function computing the Spot Incl Signals
        :param spot_incl_costs: values of spot_incl_costs
        :param inverse_volatility: values of inverse_volatility
        :return: a dataFrame with Spot Incl Signals  values
        """

        spot_incl_signals_values = [100]

        if self.weight == '1/N':
            average_spot_incl_signals = (spot_incl_costs / spot_incl_costs.shift(1)).mean(axis=1).iloc[1:].tolist()
            for value in range(len(average_spot_incl_signals)):
                spot_incl_signals_values.append(spot_incl_signals_values[value] * average_spot_incl_signals[value])
            # spot_incl_signals_values.pop(0)
        else:
            returns_shift = (spot_incl_costs / spot_incl_costs.shift(1)).iloc[1:]
            spot_incl_signals_values = self.compute_aggregate_inverse_volatility(returns_shift, inverse_volatility)

        return pd.DataFrame(spot_incl_signals_values, columns=[CurrencyAggregate.Spot_Incl_Signals.name], index=list(self.dates_index))

    def compute_aggregate_spot_excl_signals(self, spot_excl_costs, inverse_volatility):
        """
        Function computing the Spot Excl Signals
        :param spot_excl_costs: values of spot_excl_costs
        :param inverse_volatility: values of inverse_volatility
        :return: a dataFrame with Spot Excl Signals values
        """

        spot_excl_signals_values = [100]

        if self.weight == '1/N':
            average_spot_excl_signals = (spot_excl_costs / spot_excl_costs.shift(1)).mean(axis=1).iloc[1:].tolist()
            for value in range(len(average_spot_excl_signals)):
                spot_excl_signals_values.append(spot_excl_signals_values[value] * average_spot_excl_signals[value])
            # spot_excl_signals_values.pop(0)
        else:
            returns_shift = (spot_excl_costs / spot_excl_costs.shift(1)).iloc[1:]
            spot_excl_signals_values = self.compute_aggregate_inverse_volatility(returns_shift, inverse_volatility)

        return pd.DataFrame(spot_excl_signals_values, columns=[CurrencyAggregate.Spot_Excl_Signals.name], index=list(self.dates_index))

    @staticmethod
    def compute_log_returns_excl_costs(returns_ex_costs):
        """
        Function computing the lof of returns excl costs
        :param returns_ex_costs: returns_ex_costs values
        :return: a dataFrame with log of returns excl costs
        """

        np.seterr(divide='ignore')
        return np.log((returns_ex_costs / returns_ex_costs.shift(1)).iloc[1:])

    @staticmethod
    def compute_weighted_performance(log_returns_excl, combo_curr, weight_value):
        """
        Function comptuing the weighted performancen
        :param log_returns_excl: log of retuns excl costs values
        :param combo_curr: combo of currencies from compute_currencies class
        :param weight_value: weight value (pos attr from the inputs)
        :return: a dataFrame with weighted performance values
        """

        # We remove two lines to fit with log_returns_excl. It is due to the shift(1) in log_returns_excl
        # and to combo calculations with the first value set to 100
        combo = combo_curr.iloc[1:]

        sum_prod = []
        weighted_perf = []

        for values_combo, values_log in zip(combo.values, log_returns_excl.values):
            tmp = []
            for value_combo, value_log in zip(values_combo, values_log):
                tmp.append(np.nanprod(value_combo * value_log))

            sum_prod.append(sum(tmp))

        for value_weight in range(len(sum_prod)):
            weighted_perf.append(sum_prod[value_weight] * weight_value)

        return pd.DataFrame(weighted_perf, columns=[CurrencyAggregate.Weighted_Performance.name], index=combo.index.values)

    def run_aggregate_currencies(self, returns_incl_costs, spot_incl_costs, spot_origin, carry_origin, combo_curr, weight_value):
        """
        Function running the different function above
        :param returns_incl_costs: returns_incl_costs values
        :param spot_incl_costs: spot_incl_costs values
        :param spot_origin: spot_origin values
        :param carry_origin: carry_origin values from Bloomberg
        :param combo_curr: combo_curr values from compute currencies class
        :return: a dictionary
        """
        if self.weight != '1/N':
            inverse_volatility = self.compute_inverse_volatility(spot_data=spot_origin)
        else:
            inverse_volatility = None

        excl_signals_total_return = self.compute_excl_signals_total_return(carry_origin=carry_origin)

        excl_signals_spot_return = self.compute_excl_signals_spot_return(spot_origin=spot_origin)

        log_returns_excl_costs = self.compute_log_returns_excl_costs(returns_ex_costs=excl_signals_total_return)

        weighted_performance = self.compute_weighted_performance(log_returns_excl=log_returns_excl_costs,
                                                                 combo_curr=combo_curr, weight_value=weight_value)

        aggregate_total_incl_signals = self.compute_aggregate_total_incl_signals(returns_incl_costs=returns_incl_costs,
                                                                                 inverse_volatility=inverse_volatility)

        aggregate_total_excl_signals = self.compute_aggregate_total_excl_signals(returns_excl_costs=excl_signals_total_return,
                                                                                 inverse_volatility=inverse_volatility)

        aggregate_spot_incl_signals = self.compute_aggregate_spot_incl_signals(spot_incl_costs=spot_incl_costs,
                                                                               inverse_volatility=inverse_volatility)

        aggregate_spot_excl_signals = self.compute_aggregate_spot_excl_signals(spot_excl_costs=excl_signals_spot_return,
                                                                               inverse_volatility=inverse_volatility)

        return {'agg_total_incl_signals': aggregate_total_incl_signals,
                'agg_total_excl_signals': aggregate_total_excl_signals,
                'agg_spot_incl_signals': aggregate_spot_incl_signals,
                'agg_spot_excl_signals': aggregate_spot_excl_signals,
                'weighted_performance': weighted_performance, 'log_returns_excl_costs': log_returns_excl_costs}
