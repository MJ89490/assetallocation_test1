"""
Created on Thu Feb  13 17:39:00 2020
FICA
@author: WK68945 & AB
"""

import numpy as np
import pandas as pd
import math
from scipy.interpolate import CubicSpline

# creating dataframe with yield curve data

def format_data(fica_inputs, asset_inputs, all_data):
    # reading inputs and shortening data
    country = asset_inputs['country']
    date_from = fica_inputs['date_from'].item()
    date_to = fica_inputs['date_to'].item()
    all_data = all_data.loc[date_from:date_to]
    all_data = all_data.asfreq('BM')

    asset_inputs_t = asset_inputs.set_index('country').T

    if fica_inputs['curve'].item() == 'sovereign':
        ini = 0
    else:
        ini = 14

    # creating dataframe for first country and then loop the rest
    curve = all_data[asset_inputs_t['AUD'][ini:ini + 14]]

    for i in range(2, 11):
        curve = pd.merge(curve, all_data[asset_inputs_t[country[i]][ini:ini + 14]], right_index=True, left_index=True)

    return curve


# creating dataframe with carry + roll down and return calculations

def carry_roll_down(fica_inputs, asset_inputs, curve):
    # reading inputs
    tenor = fica_inputs['tenor'].item()
    coupon = fica_inputs['coupon'].item()
    country = asset_inputs['country']

    # creating cash flows and corresponding cash flow dates
    nodes = pd.Series(np.arange(0.5, tenor + 0.5, 0.5))
    nodes_curve = np.arange(11)
    nodes_curve = pd.Series(np.append(nodes_curve, [15, 20, 30]))
    cash_flows = pd.Series([coupon * 100 / 2] * tenor * 2)
    cash_flows[tenor * 2 - 1] = cash_flows[tenor * 2 - 1] + 100

    # calculating discount factors looping over countries, history and cash flow dates, using cubic spline
    # creating carry + roll down and present value dataframes
    n = len(curve)
    df = pd.DataFrame(np.array([np.arange(tenor * 2)] * 2).T)
    pv = pd.DataFrame(np.array([np.arange(10)] * n).T)
    pv1m = pd.DataFrame(np.array([np.arange(10)] * n).T)
    carry_roll = pd.DataFrame(np.array([np.arange(10)] * n).T, columns=curve.index)
    returns = pd.DataFrame(np.array([np.arange(10)] * n).T, columns=curve.index)
    for i in range(0, 10):
        for k in range(0, n):
            cs = CubicSpline(nodes_curve, curve.iloc[k, i * 14:i * 14 + 14])
            for j in range(0, tenor*2):
                df.iloc[j, 0] = 1 / (1 + cs(nodes[j]) / 100) ** nodes[j]
                df.iloc[j, 1] = 1 / (1 + cs(nodes[j] - 1 / 12) / 100) ** (nodes[j] - 1 / 12)
            pv.iloc[i, k] = sum(cash_flows * df.iloc[:, 0])
            pv1m.iloc[i, k] = sum(cash_flows * df.iloc[:, 1])
            carry_roll.iloc[i, k] = (pv1m.iloc[i, k] / pv.iloc[i, k]) ** 12 * 100 - 100 - curve.iloc[k, i * 14 + 1]
            if k > 0:
                returns.iloc[i, k] = math.log((pv1m.iloc[i, k] / pv.iloc[i, k - 1])) * 100 \
                                     - curve.iloc[k - 1, i * 14 + 1] / 12

    # transposing and adding column names
    carry_roll = carry_roll.T
    returns = returns.T
    returns.iloc[0, :] = np.NaN
    carry_roll.columns = country
    returns.columns = country

    return carry_roll, returns


# creating dataframe with signals and calculating performances

def signals(fica_inputs, carry_roll, returns):
    # reading inputs
    weight_1 = fica_inputs['strategy_weights_1'].item()
    weight_2 = fica_inputs['strategy_weights_2'].item()
    weight_3 = fica_inputs['strategy_weights_3'].item()
    weight_4 = fica_inputs['strategy_weights_4'].item()
    weight_5 = fica_inputs['strategy_weights_5'].item()
    weight_6 = fica_inputs['strategy_weights_6'].item()
    weight_7 = fica_inputs['strategy_weights_7'].item()
    weight_8 = fica_inputs['strategy_weights_8'].item()
    weight_9 = fica_inputs['strategy_weights_9'].item()
    weight_10 = fica_inputs['strategy_weights_10'].item()
    costs = fica_inputs['trading_costs'].item()

    # ranking the countries
    rank = carry_roll.T.rank()
    rank = rank.T
    signal = rank

    # determining country weights
    signal = signal.replace(1, weight_10)
    signal = signal.replace(2, weight_9)
    signal = signal.replace(3, weight_8)
    signal = signal.replace(4, weight_7)
    signal = signal.replace(5, weight_6)
    signal = signal.replace(6, weight_5)
    signal = signal.replace(7, weight_4)
    signal = signal.replace(8, weight_3)
    signal = signal.replace(9, weight_2)
    signal = signal.replace(10, weight_1)

    # determining country performance contributions
    contribution = returns.sub(returns.mean(axis=1), axis=0) * signal.shift()
    cum_contribution = contribution.cumsum()
    contribution['Return'] = contribution.sum(axis=1)
    cum_contribution['Return'] = cum_contribution.sum(axis=1)
    sub_signal = signal - signal.shift()
    signal['Turnover'] = sub_signal.abs().sum(axis=1)
    signal['Costs'] = signal['Turnover'] * costs / 100

    return carry_roll, returns, signal, contribution, cum_contribution


def format_daily_data_and_calcs(fica_inputs, asset_inputs, all_data, signal):
    # reading inputs and shortening data
    carry = pd.DataFrame()

    country = asset_inputs['country']
    date_from = fica_inputs['date_from'].item()
    date_to = fica_inputs['date_to'].item()
    all_data = all_data.loc[date_from:date_to]

    asset_inputs_t = asset_inputs.set_index('country').T

    # creating dataframe for first country and then loop the rest plus 3x futures tickers
    futures = all_data[asset_inputs['future_ticker'][3:6]]
    curve_ox = all_data[asset_inputs_t['AUD'][28:32]]

    for i in range(2, 11):
        curve_ox = pd.merge(curve_ox, all_data[asset_inputs_t[country[i]][28:32]], right_index=True, left_index=True)

    carry['AUD'] = 10 * curve_ox.iloc[:, 3] - 9 * curve_ox.iloc[:, 2] - curve_ox.iloc[:, 0]

    for i in range(1, 10):
        carry = pd.merge(carry, pd.Series((10 * curve_ox.iloc[:, 3 + i * 4] - 9 * curve_ox.iloc[:, 2 + i * 4]
                - curve_ox.iloc[:, i * 4]), name=country[i + 1]), right_index=True, left_index=True)

    carry.columns = country

    # creating daily signals from monthly signals
    signal_daily = signal.resample('B').ffill()


    return carry, futures, signal_daily

