"""
Created on Tue May  26 15:58:00 2020
FICA
@author: WK68945 & JF12345
"""

import numpy as np
import pandas as pd


def format_data(maven_inputs, asset_inputs, all_data):
    # reading inputs
    date_from = maven_inputs['date_from'].item()
    date_to = maven_inputs['date_to'].item()
    all_data = all_data.loc[date_from:date_to]

    # choosing between excess and total returns, adjusting the credit excess return series
    if maven_inputs['er_tr'].item() == 'excess':
        all_data = all_data[asset_inputs['bbg_er_ticker']]
        boolean_true_excess = asset_inputs['true_excess'] == 1
        for i in range(0, len(boolean_true_excess)):
            if boolean_true_excess[i + 1] == 1:
                all_data.iloc[:, i] = 1 + all_data.iloc[:, i] / 100
    else:
        all_data = all_data[asset_inputs['bbg_tr_ticker']]

    # choosing between weekly or monthly data, splitting up assets and cash
    frequency = maven_inputs['frequency'].item()
    boolean_cash = asset_inputs['asset_class'] == 'CASH'
    boolean_assets = asset_inputs['asset_class'] != 'CASH'

    # calculate average cash rate over the period
    if frequency == 'monthly':
        assets = all_data.loc[:, boolean_assets.values].asfreq('BM')
        cash = all_data.loc[:, boolean_cash.values].resample('BM', label='right', closed='right').mean()
    else:
        assets = all_data.loc[:, boolean_assets.values].asfreq('W-' + maven_inputs['week_day'].item())
        cash = all_data.loc[:, boolean_cash.values].resample('W-' + maven_inputs['week_day'].item(),
                                                                   label='right', closed='right').mean()

    # removing last data point as the resample with label='right' creates one beyond the chosen data period
    cash = cash.loc[date_from:date_to].round(4)

    # transforming cash rates into cash index returns with cash ticker headers
    days = [np.array((cash.index - cash.index.shift(-1)).days)] * sum(boolean_cash)
    days = pd.DataFrame(np.transpose(days), columns=cash.columns, index=cash.index)
    cash = (1 + (days * cash) / 36500).cumprod()

    # merging both pandaframes
    asset_returns = pd.merge(assets, cash, right_index=True, left_index=True)

    return asset_returns


def calculating_excess_returns(maven_inputs, asset_inputs, asset_returns):
    # selecting maven assets and corresponding tickers
    if maven_inputs['er_tr'].item() == 'excess':
        maven_tickers = asset_inputs[['bbg_er_ticker', 'cash_ticker']]
    else:
        maven_tickers = asset_inputs[['bbg_tr_ticker', 'cash_ticker']]
    maven_tickers.columns = ['asset_ticker', 'cash_ticker']
    boolean_assets = asset_inputs['asset_weight'] != 0
    m = sum(boolean_assets)
    n = len(asset_returns)
    maven_tickers = maven_tickers.iloc[0: m, :]

    # creating asset excess returns
    assets = asset_returns[maven_tickers['asset_ticker']]
    boolean_true_excess = asset_inputs['true_excess'] == 1
    #
    if boolean_true_excess[1] == 1 and maven_inputs['er_tr'].item() == 'excess':
        cash = np.ones(n)
    else:
        cash = asset_returns[maven_tickers['cash_ticker'][1]].to_numpy()
    for i in range(2, m + 1):
        if boolean_true_excess[i] == 1 and maven_inputs['er_tr'].item() == 'excess':
            cash = np.column_stack((cash, np.ones(n)))
        else:
            cash = np.column_stack((cash, asset_returns[maven_tickers['cash_ticker'][i]].to_numpy()))
    #
    cash = pd.DataFrame(cash)
    cash.index = assets.index
    cash.columns = assets.columns

    # excess returns
    asset_excess = (assets / assets.shift()) / (cash / cash.shift())

    # combining combination assets (e.g. periphery)
    asset_excess = asset_excess.to_numpy()
    maven_assets = asset_inputs['asset']
    maven_weight = asset_inputs['asset_weight']
    maven_assets = maven_assets[0: m]
    m_u = len(maven_assets.unique())
    #
    asset_unique = np.ones([n, m_u])
    count = 0
    asset_unique[:, 0] = asset_excess[:, 0] * maven_weight[1]
    for i in range(1, m):
        if maven_assets[i + 1] != maven_assets[i]:
            asset_unique[:, i - count] = asset_excess[:, i] * maven_weight[i + 1]
        else:
            asset_unique[:, i - count - 1] = asset_unique[:, i - count - 1] + asset_excess[:, i] * maven_weight[i + 1]
            count = count + 1
    #
    asset_unique[0, :] = 100
    maven_returns = pd.DataFrame(asset_unique, index=asset_returns.index , columns=maven_assets.unique())
    maven_returns = maven_returns.cumprod()

    return maven_returns


def calculating_signals(maven_inputs, asset_inputs, maven_returns):

    n = len(maven_returns)
    mom_weight = [maven_inputs['momentum_weight_' + str(x) + 'm'].item() for x in range(1, 7)]
    vol_weight = [maven_inputs['volatility_weight_' + str(x) + 'y'].item() for x in range(1, 6)]
    val_period = maven_inputs['val_period_months'].item()
    base = maven_inputs['val_period_base'].item()
    long_cutoff = maven_inputs['long_cutoff'].item()
    short_cutoff = maven_inputs['short_cutoff'].item()
    nr_long = maven_inputs['nr_long_assets'].item()
    nr_short = maven_inputs['nr_short_assets'].item()
    #
    maven_prc = maven_returns.pct_change()
    maven_sqr = maven_returns.pct_change() ** 2
    #
    volatility = 12 ** 0.5 * ((vol_weight[0] * maven_sqr.shift(0).rolling(12).sum() +   \
                               vol_weight[1] * maven_sqr.shift(12).rolling(12).sum() +  \
                               vol_weight[2] * maven_sqr.shift(24).rolling(12).sum() +  \
                               vol_weight[3] * maven_sqr.shift(36).rolling(12).sum() +  \
                               vol_weight[4] * maven_sqr.shift(48).rolling(12).sum()) / (12 * sum(vol_weight)) - \
                             ((vol_weight[0] * maven_prc.shift(0).rolling(12).mean()  + \
                               vol_weight[1] * maven_prc.shift(12).rolling(12).mean() + \
                               vol_weight[2] * maven_prc.shift(24).rolling(12).mean() + \
                               vol_weight[3] * maven_prc.shift(36).rolling(12).mean() + \
                               vol_weight[4] * maven_prc.shift(48).rolling(12).mean()) / sum(vol_weight)) ** 2) ** 0.5
    #
    momentum = (((1 + maven_prc.shift(0)) ** mom_weight[0] * \
                 (1 + maven_prc.shift(1)) ** mom_weight[1] * \
                 (1 + maven_prc.shift(2)) ** mom_weight[2] * \
                 (1 + maven_prc.shift(3)) ** mom_weight[3] * \
                 (1 + maven_prc.shift(4)) ** mom_weight[4] * \
                 (1 + maven_prc.shift(5)) ** mom_weight[5]) ** (12 / sum(mom_weight)) - 1) / volatility
    #
    value = -((maven_returns / maven_returns.shift(int(val_period - base / 2)).rolling(base).mean()) \
                                                                        ** (12 / val_period) - 1) / volatility
    #
    long_signals = value.applymap(lambda x: -999 if x < -1 * long_cutoff else x)
    short_signals = value.applymap(lambda x: -999 if x > short_cutoff else -x)
    asset_long = value_long.rank(axis=1)
    asset_short = value_short.rank(axis=1)


    return momentum, value