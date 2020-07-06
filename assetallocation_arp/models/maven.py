"""
Created on Tue May  26 15:58:00 2020
FICA
@author: WK68945 & JF12345
"""

import numpy as np
import pandas as pd

from assetallocation_arp.models import portfolio_construction as pc


def format_data(maven_inputs, asset_inputs, all_data):
    """
    creating dataframe with asset return index series
    :param pd.DataFrame maven_inputs: parameter choices for the model
    :param pd.DataFrame asset_inputs: asset bloomberg tickers
    :param pd.DataFrame all_data: historical bloomberg time series
    :return: dataframe with formatted asset return series
    """
    # reading inputs
    all_data.iloc[-1:] = all_data.iloc[-2:].fillna(method='ffill').tail(1)
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
    days = pd.DataFrame(data=np.transpose(days), columns=cash.columns, index=cash.index)
    cash = (1 + (days * cash) / 36500).cumprod()
    # merging both dataframes
    asset_returns = pd.merge(assets, cash, right_index=True, left_index=True)
    return asset_returns


def calculate_excess_returns(maven_inputs, asset_inputs, asset_returns):
    """
    creating dataframe with maven's excess return index series
    :param pd.DataFrame maven_inputs: parameter choices for the model
    :param pd.DataFrame asset_inputs: asset bloomberg tickers
    :param pd.DataFrame asset_returns: formatted asset return series
    :return: dataframe with formatted return series for maven assets
    """
    # selecting maven assets and corresponding tickers
    if maven_inputs['er_tr'].item() == 'excess':
        maven_tickers = asset_inputs[['bbg_er_ticker', 'cash_ticker']]
    else:
        maven_tickers = asset_inputs[['bbg_tr_ticker', 'cash_ticker']]
    # just changing one column header
    maven_tickers.columns = ['asset_ticker', 'cash_ticker']
    # determining the non-cash assets
    boolean_assets = asset_inputs['asset_weight'] != 0
    m = sum(boolean_assets)     # number of assets
    n = len(asset_returns)      # number of observations
    maven_tickers = maven_tickers.iloc[0: m, :]
    # creating asset excess returns
    assets = asset_returns[maven_tickers['asset_ticker']]
    boolean_true_excess = asset_inputs['true_excess'] == 1
    if boolean_true_excess[1] == 1 and maven_inputs['er_tr'].item() == 'excess':
        cash = np.ones(n)
    else:
        cash = asset_returns[maven_tickers['cash_ticker'][1]].to_numpy()
    for i in range(2, m + 1):
        if boolean_true_excess[i] == 1 and maven_inputs['er_tr'].item() == 'excess':
            cash = np.column_stack((cash, np.ones(n)))
        else:
            cash = np.column_stack((cash, asset_returns[maven_tickers['cash_ticker'][i]].to_numpy()))
    cash = pd.DataFrame(data=cash, index=assets.index, columns=assets.columns)
    asset_excess = (assets / assets.shift()) / (cash / cash.shift())
    # combining combination assets (e.g. periphery)
    asset_excess = asset_excess.to_numpy()
    maven_assets = asset_inputs['asset'][0: m]
    maven_weight = asset_inputs['asset_weight']
    asset_unique = np.ones([n, len(maven_assets.unique())])
    count = 0
    asset_unique[:, 0] = asset_excess[:, 0] * maven_weight[1]
    for i in range(1, m):
        if maven_assets[i + 1] != maven_assets[i]:
            asset_unique[:, i - count] = asset_excess[:, i] * maven_weight[i + 1]
        else:
            asset_unique[:, i - count - 1] = asset_unique[:, i - count - 1] + asset_excess[:, i] * maven_weight[i + 1]
            count = count + 1
    # replacing nan with start index value of 100
    asset_unique[0, :] = 100
    maven_returns = pd.DataFrame(data=asset_unique, index=asset_returns.index, columns=maven_assets.unique()).cumprod()
    return maven_returns


def calculate_signals(maven_inputs, maven_returns):
    """
    creating dataframes with value and momentum scores, and the top/bottom countries on the combination score
    :param pd.DataFrame maven_inputs: parameter choices for the model
    :param pd.DataFrame maven_returns: formatted return series for maven assets
    :return: dataframes with momentum and value scores, volatility matrix, and long and short signals
    """
    # reading inputs
    mom_weight = [maven_inputs['momentum_weight_' + str(x) + 'm'].item() for x in range(1, 7)]
    vol_weight = [maven_inputs['volatility_weight_' + str(x) + 'y'].item() for x in range(1, 6)]
    long_cutoff = maven_inputs['long_cutoff'].item()
    short_cutoff = maven_inputs['short_cutoff'].item()
    number_signals = maven_inputs['number_assets'].item()
    # transforming to returns and returns^2
    maven_prc = maven_returns.pct_change()
    maven_sqr = maven_returns.pct_change() ** 2
    # getting inputs for rolling volatility and momentum score calculations
    frequency = maven_inputs['frequency'].item()
    if frequency == 'monthly':
        n = 12      # 12months
        a = 12      # 12 sets of 1 month
    else:
        n = 52      # 52 weeks
        a = 13      # 13 sets of 4 weeks
    m = int(maven_inputs['val_period_months'].item() / 12 * n)      # look-back period for value
    base = int(maven_inputs['val_period_base'].item() / 12 * n)     # period around look-back point
    # calculating rolling volatility
    vol1 = 0
    vol2 = 0
    for i in range(0, len(vol_weight)):
        vol1 = vol1 + vol_weight[i] * maven_sqr.shift(i * n).rolling(n).mean()
        vol2 = vol2 + vol_weight[i] * maven_prc.shift(i * n).rolling(n).mean()
    volatility = n ** 0.5 * (vol1 / sum(vol_weight) - (vol2 / sum(vol_weight)) ** 2) ** 0.5
    # calculating momentum signal
    mom = 1
    for i in range(0, len(mom_weight)):
        mom = mom * (maven_returns.shift(int(i * n / a)) / maven_returns.shift(int((i + 1) * n / a))) ** mom_weight[i]
    momentum = (mom ** (a / sum(mom_weight)) - 1) / volatility
    # calculating the value scores
    value = ((maven_returns / maven_returns.shift(int(m - base / 2)).rolling(base + 1).mean()) ** (n / m) - 1) / volatility
    # shorting the dataframes
    start_date = value.first_valid_index()
    value = value[start_date:]
    momentum = momentum[start_date:]
    n = len(value)
    value_last = value.iloc[n - 1, :]
    momentum_last = momentum.iloc[n - 1, :].rename('momentum')
    # sorting last observation on momentum and applying value filter for charting purposes
    filter1 = ((value_last > long_cutoff) * momentum_last).rename('too expensive')
    filter2 = ((value_last < short_cutoff) * momentum_last).rename('too cheap')
    momentum_last = pd.concat([momentum_last, filter1, filter2], axis=1)
    value_last = value_last.sort_values()
    momentum_last = momentum_last.sort_values(by=['momentum'])
    momentum_last['momentum'] = momentum_last['momentum'] - momentum_last['too expensive'] - momentum_last['too cheap']
    # determine signals based on a combination of momentum and value scores: value filter results in -999 scores
    drop_value = (value > long_cutoff) * -999
    keep_momentum = (value <= long_cutoff) * momentum
    long_signals = drop_value + keep_momentum
    drop_value = (value < short_cutoff) * -999
    keep_momentum = (value >= short_cutoff) * -momentum
    short_signals = drop_value + keep_momentum
    # ranking signals
    long_signals_rank = long_signals.rank(axis=1, method='first', ascending=False)
    short_signals_rank = short_signals.rank(axis=1, method='first', ascending=False)
    # determining aggregate exposures for mainly the weekly model
    if frequency == 'monthly':
        w_m = 1
    else:
        w_m = 4
    long_list = long_signals_rank.iloc[n - w_m: n, :] <= number_signals
    short_list = short_signals_rank.iloc[n - w_m: n, :] <= number_signals
    long_list = long_list.sum(axis=0)
    short_list = short_list.sum(axis=0)
    long_list = long_list[long_list != 0]
    short_list = short_list[short_list != 0]
    # filtering and getting names of top assets
    long_signals_name = pd.DataFrame(np.ones((n, number_signals)), index=value.index)
    short_signals_name = pd.DataFrame(np.ones((n, number_signals)), index=value.index)
    for i in range(0, number_signals):
        long_signals_name.iloc[:, i] = long_signals_rank.apply(lambda x: x[x == i + 1].idxmin(), axis=1)
        short_signals_name.iloc[:, i] = short_signals_rank.apply(lambda x: x[x == i + 1].idxmin(), axis=1)
    return momentum, value, long_signals, short_signals, long_signals_name, short_signals_name, value_last, \
                                                momentum_last, long_list, short_list, volatility


def run_performance_stats(maven_inputs, asset_inputs, maven_returns, volatility, long_signals, short_signals):
    """
    creating dataframes with maven return series, and benchmarks, asset class exposures and contributions
    :param pd.DataFrame maven_inputs: parameter choices for the model
    :param pd.DataFrame asset_inputs: asset bloomberg tickers
    :param pd.DataFrame maven_returns: formatted return series for maven assets
    :param pd.DataFrame volatility: volatility matrix
    :param pd.DataFrame long_signals: asset long signals
    :param pd.DataFrame short_signals: asset short signals
    :return: dataframes with maven return series, asset class exposures and contributions
    """
    # reading inputs and aligning dataframes
    frequency = maven_inputs['frequency'].item()
    if frequency == 'monthly':
        w_m = 1
    else:
        w_m = 4
    m = len(maven_returns.columns)  # number of assets
    n = len(long_signals)           # number of observations
    number_signals = maven_inputs['number_assets'].item()
    maven_returns = maven_returns.tail(n)
    volatility = volatility.tail(n)
    # determining equal weights and equal volatility weights
    equal_notional = pd.DataFrame((1 / m) * np.ones((n, m)), index=long_signals.index, columns=long_signals.columns)
    equal_risk = ((1 / volatility).T / (1 / volatility).sum(axis=1)).T
    # determining benchmark returns, fully invested across all assets
    returns_en = maven_returns.pct_change() * equal_notional.shift().rolling(w_m).mean()
    returns_er = maven_returns.pct_change() * equal_risk.shift().rolling(w_m).mean()
    returns_en.iloc[0, :] = 0
    returns_er.iloc[0, :] = 0
    returns_en_cum = (1 + returns_en.sum(axis=1)).cumprod() * 100
    returns_er_cum = (1 + returns_er.sum(axis=1)).cumprod() * 100
    returns_maven = pd.DataFrame({'equal notional': returns_en_cum, 'equal volatility': returns_er_cum})
    # calculating maven long and short weights
    long_exposures = long_signals.rank(axis=1, method='first', ascending=False) <= number_signals
    short_exposures = short_signals.rank(axis=1, method='first', ascending=False) <= number_signals
    vol_long = long_exposures * (1 / volatility)
    vol_short = short_exposures * (1 / volatility)
    # capping asset weight to 50%
    equal_risk_long = pc.cap_and_redistribute((vol_long.T / vol_long.sum(axis=1)).T, 0.5).rolling(w_m).mean()
    equal_risk_short = pc.cap_and_redistribute((vol_short.T / vol_short.sum(axis=1)).T, 0.5).rolling(w_m).mean()
    # calculating turnover
    costs = asset_inputs.groupby('asset').first(keep='first')['transaction_costs'][equal_risk.columns].tolist()
    sub_equal_risk_long = equal_risk_long - equal_risk_long.shift()
    sub_equal_risk_short = equal_risk_short - equal_risk_short.shift()
    turnover_cost_long = sub_equal_risk_long.abs().mul(costs, axis=1).sum(axis=1) / 10000
    turnover_cost_short = sub_equal_risk_short.abs().mul(costs, axis=1).sum(axis=1) / 10000
    # calculating maven long and short returns, gross and net
    returns_maven_long = maven_returns.pct_change() * equal_risk_long.shift()
    returns_maven_short = maven_returns.pct_change() * -equal_risk_short.shift()
    returns_maven_long.iloc[0, :] = 0
    returns_maven_short.iloc[0, :] = 0
    returns_maven['maven long gross'] = (1 + returns_maven_long.sum(axis=1)).cumprod() * 100
    returns_maven['maven short gross'] = (1 + returns_maven_short.sum(axis=1)).cumprod() * 100
    returns_maven['maven long net'] = (1 + returns_maven_long.sum(axis=1) - turnover_cost_long).cumprod() * 100
    returns_maven['maven short net'] = (1 + returns_maven_short.sum(axis=1) - turnover_cost_short).cumprod() * 100
    # determining asset class contributions
    asset_class = asset_inputs.groupby('asset').first(keep='first')['asset_class'][equal_risk.columns].tolist()
    asset_contribution_long = pd.DataFrame(data=returns_maven_long.T)
    asset_contribution_long.index = asset_class
    asset_contribution_short = pd.DataFrame(data=returns_maven_short.T)
    asset_contribution_short.index = asset_class
    asset_contribution_long = asset_contribution_long.groupby(asset_contribution_long.index).sum().T
    asset_contribution_short = asset_contribution_short.groupby(asset_contribution_short.index).sum().T
    # determining asset class weights
    asset_class_long = pd.DataFrame(data=equal_risk_long.T)
    asset_class_long.index = asset_class
    asset_class_short = pd.DataFrame(data=equal_risk_short.T)
    asset_class_short.index = asset_class
    asset_class_long = asset_class_long.groupby(asset_class_long.index).sum().T
    asset_class_short = asset_class_short.groupby(asset_class_short.index).sum().T
    return returns_maven, asset_class_long, asset_class_short, asset_contribution_long, asset_contribution_short