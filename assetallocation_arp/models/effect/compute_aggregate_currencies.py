
import pandas as pd
import statistics as stats
import math
import numpy as np
#todo crceate a class


def compute_inverse_volatility(spot_data, start_date, window, index):

    inverse_volatilities = pd.DataFrame()

    for currency_spot in spot_data.columns:

        tmp_start_date_computations = start_date
        rows = spot_data[tmp_start_date_computations:].shape[0]

        spot_tmp = spot_data.loc[:, currency_spot]
        volatilities = []

        for value in range(rows):
            # Set the start date to start the computation
            start_current_date_index_loc = spot_data.index.get_loc(tmp_start_date_computations)
            start_current_date_index = spot_data.index[start_current_date_index_loc]

            # Take previous date depending on the size of the window
            previous_start_date_index = spot_data.index[start_current_date_index_loc - window]
            previous_start_date_index_loc = spot_data.index.get_loc(previous_start_date_index)

            # Take the previous values depending on the size of the window
            values_window = spot_tmp[previous_start_date_index:start_current_date_index]

            values_rolling_window = values_window / values_window.shift(1)

            # Compute the standard deviation and the inverse volatility per currency
            try:
                volatility = 1 / (math.sqrt(52) * stats.stdev(values_rolling_window.iloc[1:]))
            except ZeroDivisionError:
                volatility = float("Nan")

            # Add the standard deviation results into a list
            volatilities.append(volatility)

            # Error handling when we reach the end of the dates range
            try:
                tmp_start_date_computations = spot_data.index[start_current_date_index_loc + 1]
            except IndexError:
                tmp_start_date_computations = spot_data.index[start_current_date_index_loc]

        # Add volatilities into a common dataFrame
        inverse_volatilities['Inverse_Volatility_' + currency_spot] = volatilities

    inverse_volatilities = inverse_volatilities.set_index(index)

    return inverse_volatilities


def compute_excl_signals_total_return(carry_data, start_date):
    """
    Function computing Excl signals (total return) dividing the current value by the start date value
    :param carry_data: carry data from Bloomberg for all currencies
    :param start_date: start date of calculations
    :return: dataFrame of Excl signals (total return)
    """

    return (carry_data.loc[start_date:] / carry_data.loc[start_date]).apply(lambda x: x * 100)


def compute_excl_signals_spot_return(spot_data, start_date):
    """
    Function computing Excl signals (spot return) dividing the current value by the start date value
    :param spot_data: spot data from Blommberg for all currencies
    :param start_date: start date of calculations
    :return: dataFrame of Excl signals (spot return)
    """

    return (spot_data.loc[start_date:] / spot_data.loc[start_date]).apply(lambda x: x * 100)


def compute_aggregate_total_incl_signals(weight, returns_incl_costs, date, index):

    first_total_signals = [100]
    total_incl_signals = pd.DataFrame()

    if weight == '1/N':
        average_incl_signals = (returns_incl_costs.loc[date:] / returns_incl_costs.loc[date:].shift(1)).mean(axis=1).iloc[1:].tolist()
        for value in range(len(average_incl_signals)):
            first_total_signals.append(first_total_signals[value] * average_incl_signals[value])

        total_incl_signals['Total_Incl_Signals'] = first_total_signals

    total_incl_signals = total_incl_signals.set_index(index)

    return total_incl_signals


def compute_aggregate_total_excl_signals(weight, returns_excl_costs, date, index):

    first_total_signals = [100]
    total_excl_signals = pd.DataFrame()

    if weight == '1/N':
        average_excl_signals = (returns_excl_costs.loc[date:] / returns_excl_costs.loc[date:].shift(1)).mean(axis=1).iloc[1:].tolist()
        for value in range(len(average_excl_signals)):
            first_total_signals.append(first_total_signals[value] * average_excl_signals[value])

        total_excl_signals['Total_Excl_Signals'] = first_total_signals

    total_excl_signals = total_excl_signals.set_index(index)

    return total_excl_signals


def compute_aggregate_spot_incl_signals(weight, spot_incl_costs, date, index):

    first_spot_incl_signals = [100]
    spot_incl_signals = pd.DataFrame()

    if weight == '1/N':
        average_spot_incl_signals = (spot_incl_costs.loc[date:] / spot_incl_costs.loc[date:].shift(1)).mean(axis=1).iloc[1:].tolist()
        for value in range(len(average_spot_incl_signals)):
            first_spot_incl_signals.append(first_spot_incl_signals[value] * average_spot_incl_signals[value])

        spot_incl_signals['Spot_Incl_Signals'] = first_spot_incl_signals

    spot_incl_signals = spot_incl_signals.set_index(index)

    return spot_incl_signals


def compute_aggregate_spot_excl_signals(weight, spot_excl_costs, date, index):

    first_spot_excl_signals = [100]
    spot_excl_signals = pd.DataFrame()

    if weight == '1/N':
        average_spot_excl_signals = (spot_excl_costs.loc[date:] / spot_excl_costs.loc[date:].shift(1)).mean(axis=1).iloc[1:].tolist()
        for value in range(len(average_spot_excl_signals)):
            first_spot_excl_signals.append(first_spot_excl_signals[value] * average_spot_excl_signals[value])

        spot_excl_signals['Spot_Excl_Signals'] = first_spot_excl_signals

    spot_excl_signals = spot_excl_signals.set_index(index)

    return spot_excl_signals


def compute_log_returns_excl_costs(returns_ex_costs):

    return np.log((returns_ex_costs / returns_ex_costs.shift(1)).iloc[1:])


def compute_weighted_performance(index, log_returns_excl, combo):

    start_date_weighted_performance = pd.to_datetime('24-07-2003', format='%d-%m-%Y')
    index_weighted_performance = pd.DataFrame(index, columns=['Dates_Weighted_Performance'])

    index_weighted_performance[index_weighted_performance.Dates_Weighted_Performance >= start_date_weighted_performance]


    log_returns_excl = log_returns_excl.loc[start_date_weighted_performance:]
    combo = combo.loc[start_date_weighted_performance:]

    from configparser import ConfigParser
    import os
    import json

    # Instantiate ConfigParser
    config = ConfigParser()
    # Parse existing file
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'matr_weights_effect.ini'))
    config.read(path)
    json.loads(config.get('weighted_performance', 'weights'))


    sum_product = combo.values.dot(log_returns_excl.values)

    return sum_product


def run_aggregate_currencies(weight, returns_incl_costs, spot_incl_costs, date, spot_data, window, index, carry_data, combo):
    inverse_volatilies = compute_inverse_volatility(spot_data=spot_data, window=window, start_date=date, index=index)

    excl_signals_total_return = compute_excl_signals_total_return(start_date=date, carry_data=carry_data)
    excl_signals_spot_return = compute_excl_signals_spot_return(start_date=date, spot_data=spot_data)

    log_returns_excl_costs = compute_log_returns_excl_costs(returns_ex_costs=excl_signals_total_return)
    weighted_performance = compute_weighted_performance(index=index, log_returns_excl=log_returns_excl_costs, combo=combo)

    aggregate_total_incl_signals = compute_aggregate_total_incl_signals(weight=weight, returns_incl_costs=returns_incl_costs, date=date, index=index)
    aggregate_total_excl_signals = compute_aggregate_total_excl_signals(weight=weight, returns_excl_costs=excl_signals_total_return, date=date, index=index)

    aggregate_spot_incl_signals = compute_aggregate_spot_incl_signals(weight=weight, spot_incl_costs=spot_incl_costs, date=date, index=index)
    aggregate_spot_excl_signals = compute_aggregate_spot_excl_signals(weight=weight, spot_excl_costs=excl_signals_spot_return, date=date, index=index)

    return {'agg_total_incl_signals': aggregate_total_incl_signals, 'agg_total_excl_signals': aggregate_total_excl_signals,
            'agg_spot_incl_signals': aggregate_spot_incl_signals, 'agg_spot_excl_signals': aggregate_spot_excl_signals,
            'weighted_perfomance': weighted_performance
           }
