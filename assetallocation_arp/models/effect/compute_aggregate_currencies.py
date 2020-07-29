
import pandas as pd
import statistics as stats
import math

#todo crceate a class


def compute_total_incl_signals(weight, returns_incl_costs, date, index):

    first_total_signals = [100]
    total_incl_signals = pd.DataFrame()

    if weight == '1/N':
        average_incl_signals = (returns_incl_costs.loc[date:] / returns_incl_costs.loc[date:].shift(1)).mean(axis=1).iloc[1:].tolist()
        for value in range(len(average_incl_signals)):
            first_total_signals.append(first_total_signals[value] * average_incl_signals[value])

        total_incl_signals['Total_Incl_Signals'] = first_total_signals

    total_incl_signals = total_incl_signals.set_index(index)

    return total_incl_signals


def compute_spot_incl_signals(weight, spot_incl_costs, date, index):

    first_spot_incl_signals = [100]
    spot_incl_signals = pd.DataFrame()

    if weight == '1/N':
        average_spot_incl_signals = (spot_incl_costs.loc[date:] / spot_incl_costs.loc[date:].shift(1)).mean(axis=1).iloc[1:].tolist()
        for value in range(len(average_spot_incl_signals)):
            first_spot_incl_signals.append(first_spot_incl_signals[value] * average_spot_incl_signals[value])

        spot_incl_signals['Spot_Incl_Signals'] = first_spot_incl_signals

    spot_incl_signals = spot_incl_signals.set_index(index)

    return spot_incl_signals


def compute_inverse_volatility(spot, start_date, window, index):

    inverse_volatilities = pd.DataFrame()

    for currency_spot in spot.columns:

        tmp_start_date_computations = start_date
        rows = spot[tmp_start_date_computations:].shape[0]

        spot_tmp = spot.loc[:, currency_spot]
        volatilities = []

        for value in range(rows):
            # Set the start date to start the computation
            start_current_date_index_loc = spot.index.get_loc(tmp_start_date_computations)
            start_current_date_index = spot.index[start_current_date_index_loc]

            # Take previous date depending on the size of the window
            previous_start_date_index = spot.index[start_current_date_index_loc - window]
            previous_start_date_index_loc = spot.index.get_loc(previous_start_date_index)

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
                tmp_start_date_computations = spot.index[start_current_date_index_loc + 1]
            except IndexError:
                tmp_start_date_computations = spot.index[start_current_date_index_loc]

        # Add volatilities into a common dataFrame
        inverse_volatilities['Inverse_Volatility_' + currency_spot] = volatilities

    inverse_volatilities = inverse_volatilities.set_index(index)

    return inverse_volatilities


def compute_log_returns_ex_costs():
    pass


def compute_weighted_performance():
    pass


def compute_total_returns_excl_signals():
    pass


def compute_spot_returns_excl_signals():
    pass


def run_aggregate_currencies(weight, returns_incl_costs, spot_incl_costs, date, spot, window, index):
    total_incl_signals = compute_total_incl_signals(weight=weight, returns_incl_costs=returns_incl_costs, date=date, index=index)
    inverse_volatilies = compute_inverse_volatility(spot=spot, window=window, start_date=date, index=index)
    spot_incl_signals = compute_spot_incl_signals(weight=weight, spot_incl_costs=spot_incl_costs, date=date, index=index)

    return {'total_incl_signals': total_incl_signals, 'spot_incl_signals':spot_incl_signals}
