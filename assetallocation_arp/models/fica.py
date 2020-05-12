"""
Created on Thu Feb  13 17:39:00 2020
FICA
@author: WK68945 & AB
"""

import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline

def format_data_and_calc(fica_inputs, asset_inputs, all_data):

    curve = pd.DataFrame()
    carry = pd.DataFrame()

    c_type = fica_inputs['curve'].item()
    date_from = fica_inputs['date_from'].item()
    date_to = fica_inputs['date_to'].item()
    country = asset_inputs['country']
    tenor = asset_inputs['tenor']

    all_data = all_data.loc[date_from:date_to]
    all_data = all_data.asfreq('BM')

    asset_inputs_t = asset_inputs.set_index('country').T

    if c_type == 'sovereign':
        start = 0
    else:
        start = 14

    curve = all_data[asset_inputs_t['AUD'][start:start+14]]
    carry = all_data[asset_inputs_t['AUD'][28:32]]

    for i in range(2, 11):
        curve = pd.merge(curve, all_data[asset_inputs_t[country[i]][start:start+14]], right_index=True, left_index=True)

    for i in range(2, 11):
        carry = pd.merge(carry, all_data[asset_inputs_t[country[i]][28:32]], right_index=True, left_index=True)

    pewe = np.arange(0, 30, 0.5).tolist()

    return curve, carry