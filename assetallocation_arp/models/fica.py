"""
Created on Thu Feb  13 17:39:00 2020
FICA
@author: WK68945 & AB
"""

import pandas as pd

def format_data(fica_inputs, asset_inputs, all_data):

    curve = pd.DataFrame()
    carry = pd.DataFrame()

    T = ['3m', '1y', '2y', '3y', '4y', '5y', '6y', '7y', '8y', '9y', '10y', '15y', '20y', '30y']
    T_c = ['3m', '1y', '9y', '10y']
    country = asset_inputs['country']
    type = fica_inputs['curve'].item()
    date_from = fica_inputs['date_from'].item()
    date_to = fica_inputs['date_to'].item()
    asset_inputs_t = asset_inputs.set_index('country').T

    all_data = all_data.loc[date_from:date_to]
    all_data = all_data.asfreq('BM')

    curve = all_data[asset_inputs[type + '_ticker_' + T[0]]]
    carry = all_data[asset_inputs['cr_swap_ticker_' + T_c[0]]]

    for i in range(1, 14):
        curve = pd.merge(curve, all_data[asset_inputs[type+'_ticker_'+T[i]]], right_index=True, left_index=True)

    for i in range(1, 4):
        carry = pd.merge(carry, all_data[asset_inputs['cr_swap_ticker_'+T_c[i]]], right_index=True, left_index=True)

    return curve, carry