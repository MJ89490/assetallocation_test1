"""
Created on Tue May  26 15:58:00 2020
FICA
@author: WK68945 & JF12345
"""

import numpy as np
import pandas as pd


def format_data(maven_inputs, asset_inputs, all_data):
    # creating dataframe with index return data for assets and cash rates
    # reading inputs, shortening data
    date_from = maven_inputs['date_from'].item()
    date_to = maven_inputs['date_to'].item()
    all_data = all_data.loc[date_from:date_to]
    # choosing between excess and total returns, weekly or monthly data
    if maven_inputs['er_tr'].item() == 'excess':
        all_data = all_data[asset_inputs['bbg_er_ticker']]
    else:
        all_data = all_data[asset_inputs['bbg_tr_ticker']]
    # choosing between weekly or monthly data, splitting up assets and cash
    frequency = maven_inputs['frequency'].item()
    count_cash = asset_inputs['asset_class'].str.count('CASH').sum()
    select_cash = asset_inputs['asset_class'] == 'CASH'
    select_assets = asset_inputs['asset_class'] != 'CASH'
    currency_names = asset_inputs['currency'][select_cash]
    # calculate average cah rate over the period
    if frequency == 'monthly':
        maven_assets = all_data.loc[:, select_assets.values].asfreq('BM')
        maven_cash = all_data.loc[:, select_cash.values].resample('BM', label='right', closed='right').mean()
    else:
        maven_assets = all_data.loc[:, select_assets.values].asfreq('W-' + maven_inputs['week_day'].item())
        maven_cash = all_data.loc[:, select_cash.values].resample('W-' + maven_inputs['week_day'].item(), label='right',
                                                                  closed='right').mean()
    #
    maven_cash = maven_cash.loc[date_from:date_to].round(4)
    # transforming cash rates into cash index returns with currency column names
    days = [np.array((maven_cash.index - maven_cash.index.shift(-1)).days)] * count_cash
    days = pd.DataFrame(np.transpose(days))
    days.columns = maven_cash.columns
    days.index = maven_cash.index
    maven_cash = (1 + (days * maven_cash) / 36500).cumprod()
    maven_cash.columns = currency_names

    return maven_assets, maven_cash
