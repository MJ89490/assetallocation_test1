"""
Created on Thu Feb  13 17:39:00 2020
FICA
@author: WK68945 & AB
"""

import numpy as np
import pandas as pd
from datetime import datetime
from datetime import timedelta
from scipy.interpolate import CubicSpline


def format_data_and_calc(fica_inputs, asset_inputs, all_data):
    curve = pd.DataFrame()
    carry = pd.DataFrame()

    date_from = fica_inputs['date_from'].item()
    date_to = fica_inputs['date_to'].item()
    all_data = all_data.loc[date_from:date_to]
    all_data = all_data.asfreq('BM')

    tenor = fica_inputs['tenor'].item()
    coupon = fica_inputs['coupon'].item()
    country = asset_inputs['country']

    asset_inputs_t = asset_inputs.set_index('country').T

    if fica_inputs['curve'].item() == 'sovereign':
        start = 0
    else:
        start = 14

    curve = all_data[asset_inputs_t['AUD'][start:start + 14]]
    carry = all_data[asset_inputs_t['AUD'][28:32]]

    for i in range(2, 11):
        curve = pd.merge(curve, all_data[asset_inputs_t[country[i]][start:start + 14]], right_index=True,
                         left_index=True)

    for i in range(2, 11):
        carry = pd.merge(carry, all_data[asset_inputs_t[country[i]][28:32]], right_index=True, left_index=True)

    pw = pd.Series(np.arange(0.5, tenor + 0.5, 0.5))
    cp = pd.Series([coupon * 100 / 2] * tenor * 2)
    cp[tenor * 2 - 1] = cp[tenor * 2 - 1] + 100

    today = datetime.now().date()
    day = today.day
    month = today.month
    dat_inst = pd.Series(today + timedelta(days=180))
    dat_cur = pd.Series(today)
    dat_inst[1] = datetime(today.year + 1, month, day).date()

    for i in range(2, tenor * 2):
        if (i % 2) == 0:
            dat_inst[i] = dat_inst[i - 1] + timedelta(days=180)
        else:
            dat_inst[i] = datetime(dat_inst[i - 2].year + 1, month, day).date()

    for i in range(1, 11):
        dat_cur[i] = datetime(dat_cur[i - 1].year + 1, month, day).date()

    dat_cur[11] = datetime(dat_cur[i].year + 5, month, day).date()
    dat_cur[12] = datetime(dat_cur[i].year + 10, month, day).date()
    dat_cur[13] = datetime(dat_cur[i].year + 20, month, day).date()

    begin = datetime(1899, 12, 30).date()
    dat_inst_xl = dat_inst - begin
    dat_cur_xl = dat_cur - begin
    for i in range(0, tenor*2):
        dat_inst_xl[i] = dat_inst_xl[i].days
    for i in range(0, 14):
        dat_cur_xl[i] = dat_cur_xl[i].days

    #cs = CubicSpline(dat_cur_xl, curve.iloc[0, 0:14])
    #print(cs(dat_inst_xl))

    return curve, carry, dat_inst_xl, dat_cur_xl
