"""
Created on Thu Feb  13 17:39:00 2020
FICA
@author: WK68945 & AB12345
"""

import numpy as np
import pandas as pd
import math
from scipy.interpolate import CubicSpline


def format_data(fica_inputs, asset_inputs, all_data):
    """
    creating dataframe with yield curve data
    :param pd.DataFrame fica_inputs: parameter choices for the model
    :param pd.DataFrame asset_inputs: asset bloomberg tickers
    :param pd.DataFrame all_data: historical bloomberg time series
    :return: dataframe with historical yield curves per country
    """
    # reading inputs and shortening data
    country = asset_inputs['country']
    m = len(country)
    date_from = fica_inputs['date_from'].item()
    date_to = fica_inputs['date_to'].item()
    all_data = all_data.loc[date_from:date_to]
    all_data = all_data.asfreq('BM')
    asset_inputs_t = asset_inputs.set_index('country').T
    # selecting which yield curve to use
    if fica_inputs['curve'].item() == 'sovereign':
        ini = 0
    else:
        ini = 14
    # creating dataframe for all countries
    ticker_list = asset_inputs_t[country[1]][ini: ini + 14].tolist()
    for i in range(2, m + 1):
        ticker_list.extend(asset_inputs_t[country[i]][ini: ini + 14].tolist())
    curve = all_data[ticker_list]
    return curve


def calculate_carry_roll_down(fica_inputs, asset_inputs, curve):
    """
    creating dataframe with carry + roll down and return calculations
    :param pd.DataFrame fica_inputs: parameter choices for the model
    :param pd.DataFrame asset_inputs: asset bloomberg tickers
    :param pd.DataFrame curve: dataframe with historical yield curves per country
    :return: dataframe with historical carry and roll down and return calculations per country
    """
    # reading inputs
    tenor = fica_inputs['tenor'].item()
    coupon = fica_inputs['coupon'].item()
    country = asset_inputs['country']
    n = len(curve)
    m = len(country)
    # creating cash flows (semi-annually until expiration) and corresponding cash flow dates
    nodes = np.arange(0.5, tenor + 0.5, 0.5)
    nodes_curve = np.arange(11)
    nodes_curve = np.append(nodes_curve, [15, 20, 30])
    cash_flows = [coupon * 100 / 2] * tenor * 2
    cash_flows[tenor * 2 - 1] = cash_flows[tenor * 2 - 1] + 100
    # calculating discount factors looping over countries, history and cash flow dates, using cubic spline
    # calculating present value, carry and return series
    df = pd.DataFrame(np.array([np.arange(tenor * 2)] * 2).T)
    pv = pd.DataFrame(np.array([np.arange(m)] * n).T)
    pv1m = pd.DataFrame(np.array([np.arange(m)] * n).T)
    carry_roll = pd.DataFrame(np.array([np.arange(m)] * n).T, columns=curve.index)
    country_returns = pd.DataFrame(np.array([np.arange(m)] * n).T, columns=curve.index)
    for i in range(m):
        for k in range(n):
            cs = CubicSpline(nodes_curve, curve.iloc[k, i * 14:i * 14 + 14])
            df.iloc[:, 0] = 1 / (1 + cs(nodes) / 100) ** nodes
            df.iloc[:, 1] = 1 / (1 + cs(nodes - 1 / 12) / 100) ** (nodes - 1 / 12)
            pv.iloc[i, k] = sum(cash_flows * df.iloc[:, 0])
            pv1m.iloc[i, k] = sum(cash_flows * df.iloc[:, 1])
            carry_roll.iloc[i, k] = (pv1m.iloc[i, k] / pv.iloc[i, k]) ** 12 * 100 - 100 - curve.iloc[k, i * 14 + 1]
            if k > 0:
                country_returns.iloc[i, k] = math.log((pv1m.iloc[i, k] / pv.iloc[i, k - 1])) * 100 \
                                           - curve.iloc[k - 1, i * 14 + 1] / 12
    # transposing and adding column names
    carry_roll = carry_roll.T
    carry_roll.columns = country
    country_returns = country_returns.T
    country_returns.iloc[0, :] = np.NaN
    country_returns.columns = country
    return carry_roll, country_returns


def calculate_signals_and_returns(fica_inputs, carry_roll, country_returns):
    """"
    creating dataframe with country signals and contributions and overall model performances
    :param pd.DataFrame fica_inputs: parameter choices for the model
    :param pd.DataFrame carry_roll: historical carry and roll down calculations per country
    :param pd.DataFrame country_returns: historical return calculations per country
    :return: dataframes with monthly model signals, cumulative country contributions and model returns
    """
    # reading inputs
    returns = pd.DataFrame()
    m = len(carry_roll.columns)
    n = len(carry_roll)
    weight = [fica_inputs['strategy_weights_' + str(x)].item() for x in range(1, m + 1)]
    costs = fica_inputs['trading_costs'].item()
    # ranking the countries
    rank = carry_roll.T.rank()
    signals = rank.T
    # determining country weights
    for i in range(m):
        signals = signals.replace(i + 1, weight[m - i - 1])
    # calculating country performance contributions
    contribution = country_returns.sub(country_returns.mean(axis=1), axis=0) * signals.shift()
    cum_contribution = contribution.cumsum()
    contribution['Return'] = contribution.sum(axis=1)
    cum_contribution['Return'] = cum_contribution.sum(axis=1)
    # calculating returns, starting return index series with 100
    sub_signals = signals - signals.shift()
    signals['Turnover'] = sub_signals.abs().sum(axis=1)
    returns['Costs'] = signals['Turnover'] * costs / 100
    returns['Net_Return'] = cum_contribution['Return'] - returns['Costs'].cumsum()
    returns['Arithmetic'] = (1 + returns['Net_Return'] / 100) * 100
    returns['Geometric'] = 100
    for k in range(1, n):
        returns.iloc[k, 3] = (1 + (contribution.iloc[k, m] - returns.iloc[k, 0]) / 100) * returns.iloc[k - 1, 3]

    return signals, cum_contribution, returns


def run_daily_attribution(fica_inputs, asset_inputs, all_data, signals):
    """
    performing the daily attributions and inputs for the charts
    :param pd.DataFrame fica_inputs: parameter choices for the model
    :param pd.DataFrame asset_inputs: asset bloomberg tickers
    :param pd.DataFrame all_data: historical bloomberg time series
    :param pd.DataFrame signals: monthly model signals
    :return: dataframes with daily carry and roll down and return calculations
    """
    # reading inputs and shortening data
    carry_daily = pd.DataFrame()
    return_daily = pd.DataFrame()
    country = asset_inputs['country']
    m = len(country)
    date_from = fica_inputs['date_from'].item()
    date_to = fica_inputs['date_to'].item()
    all_data = all_data.loc[date_from:date_to]
    n = len(all_data)
    asset_inputs_t = asset_inputs.set_index('country').T
    # creating carry & return dataframe for three country proxy
    futures = all_data[asset_inputs_t.loc['future_ticker', ['EUR', 'GBP', 'USD']]]
    ticker_list = asset_inputs_t[country[1]][28:32].tolist()
    for i in range(2, m + 1):
        ticker_list.extend(asset_inputs_t[country[i]][28:32].tolist())
    curve_ox = all_data[ticker_list]
    #
    for i in range(0, m):
        carry_daily[country[i + 1]] = 10 * curve_ox.iloc[:, 3+i*4] - 9 * curve_ox.iloc[:, 2+i*4] - curve_ox.iloc[:, i*4]
        return_daily[country[i + 1]] = -7.5 * (curve_ox.iloc[:, 3+i*4] - curve_ox.iloc[:, 3+i*4].shift())
    # creating daily signals from monthly signals
    signal_daily = signals.resample('B').ffill()
    # creating FICA and G3 carry & return series
    carry_daily['fica_10y_carry'] = carry_daily.mul(signal_daily.shift()).sum(axis=1)
    carry_daily['fica_10y_carry_cum'] = carry_daily['fica_10y_carry'].cumsum() / 250
    carry_daily['G3_10y_carry'] = (carry_daily['EUR'] + carry_daily['GBP'] + carry_daily['USD']) / 3
    return_daily['fica_10y_spot'] = return_daily.mul(signal_daily.shift()).sum(axis=1)
    return_daily['fica_10y_spot_cum'] = return_daily['fica_10y_spot'].cumsum()
    return_daily['fica_10y_return'] = 100
    return_daily['G3_10y_return'] = 100
    for k in range(1, n):
        return_daily.iloc[k, m + 2] = return_daily.iloc[k - 1, m + 2] * \
                (1 + return_daily.iloc[k, m] / 100) * (1 + carry_daily.iloc[k, m] / 25000)
        return_daily.iloc[k, m + 3] = return_daily.iloc[k - 1, m + 3] * \
                futures.iloc[k, :].div(futures.iloc[k-1, :]).mean()
    return_daily['fica_10y_return%'] = return_daily['fica_10y_return'].pct_change()
    return_daily['G3_10y_return%'] = return_daily['G3_10y_return'].pct_change()
    return_daily['correlation'] = return_daily['fica_10y_return%'].rolling(64).corr(return_daily['G3_10y_return%'])
    return_daily['beta'] = return_daily['fica_10y_return%'].rolling(64).cov(return_daily['G3_10y_return%']) / \
                            return_daily['G3_10y_return%'].rolling(64).var()
    return carry_daily, return_daily