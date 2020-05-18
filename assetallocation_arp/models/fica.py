"""
Created on Thu Feb  13 17:39:00 2020
FICA
@author: WK68945 & AB
"""

import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline


def format_data(fica_inputs, asset_inputs, all_data):
    #
    curve = pd.DataFrame()
    carry = pd.DataFrame()

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

    curve = all_data[asset_inputs_t['AUD'][ini:ini + 14]]
    carry = all_data[asset_inputs_t['AUD'][28:32]]

    for i in range(2, 11):
        curve = pd.merge(curve, all_data[asset_inputs_t[country[i]][ini:ini + 14]], right_index=True, left_index=True)

    for i in range(2, 11):
        carry = pd.merge(carry, all_data[asset_inputs_t[country[i]][28:32]], right_index=True, left_index=True)

    return curve, carry


def carry_roll_down(fica_inputs, asset_inputs, curve):
    tenor = fica_inputs['tenor'].item()
    coupon = fica_inputs['coupon'].item()
    country = asset_inputs['country']

    pw = pd.Series(np.arange(0.5, tenor + 0.5, 0.5))
    pw_curve = np.arange(11)
    pw_curve = pd.Series(np.append(pw_curve, [15, 20, 30]))
    cp = pd.Series([coupon * 100 / 2] * tenor * 2)
    cp[tenor * 2 - 1] = cp[tenor * 2 - 1] + 100

    n = len(curve)
    df = pd.DataFrame(np.array([np.arange(tenor * 2)] * 2).T)
    pv = pd.DataFrame(np.array([np.arange(10)] * n).T)
    pv1m = pd.DataFrame(np.array([np.arange(10)] * n).T)
    crd = pd.DataFrame(np.array([np.arange(10)] * n).T)
    for i in range(0, 10):
        for k in range(0, n):
            cs = CubicSpline(pw_curve, curve.iloc[k, i * 14:i * 14 + 14])
            for j in range(0, tenor*2):
                df.iloc[j, 0] = 1 / (1 + cs(pw[j]) / 100) ** pw[j]
                df.iloc[j, 1] = 1 / (1 + cs(pw[j] - 1 / 12) / 100) ** (pw[j] - 1 / 12)
            pv.iloc[i, k] = sum(cp * df.iloc[:, 0])
            pv1m.iloc[i, k] = sum(cp * df.iloc[:, 1])
            crd.iloc[i, k] = (pv1m.iloc[i, k] / pv.iloc[i, k]) ** 12 * 100 - 100 - curve.iloc[k, i * 14 + 1]

    crd = crd.T
    crd.columns = country

    return crd
