"""
Created on Tue May  26 15:58:00 2020
FICA
@author: WK68945 & JF12345
"""

import numpy as np
import pandas as pd


def format_data(maven_inputs, asset_inputs, all_data):
    """
    creating dataframe with asset return index series
    :param pd.DataFrame maven_inputs: parameter choices for the model
    :param pd.DataFrame asset_inputs: asset bloomberg tickers
    :param pd.DataFrame all_data: historical bloomberg time series
    :return: dataframe with formatted asset return series
    """
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
    # merging both dataframes
    asset_returns = pd.merge(assets, cash, right_index=True, left_index=True)
    return asset_returns


def calculating_excess_returns(maven_inputs, asset_inputs, asset_returns):
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
    maven_tickers.columns = ['asset_ticker', 'cash_ticker']
    boolean_assets = asset_inputs['asset_weight'] != 0
    m = sum(boolean_assets)
    n = len(asset_returns)
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
    cash = pd.DataFrame(cash)
    cash.index = assets.index
    cash.columns = assets.columns
    asset_excess = (assets / assets.shift()) / (cash / cash.shift())
    # combining combination assets (e.g. periphery)
    asset_excess = asset_excess.to_numpy()
    maven_assets = asset_inputs['asset']
    maven_weight = asset_inputs['asset_weight']
    maven_assets = maven_assets[0: m]
    m_u = len(maven_assets.unique())
    asset_unique = np.ones([n, m_u])
    count = 0
    asset_unique[:, 0] = asset_excess[:, 0] * maven_weight[1]
    for i in range(1, m):
        if maven_assets[i + 1] != maven_assets[i]:
            asset_unique[:, i - count] = asset_excess[:, i] * maven_weight[i + 1]
        else:
            asset_unique[:, i - count - 1] = asset_unique[:, i - count - 1] + asset_excess[:, i] * maven_weight[i + 1]
            count = count + 1
    asset_unique[0, :] = 100
    maven_returns = pd.DataFrame(asset_unique, index=asset_returns.index, columns=maven_assets.unique())
    maven_returns = maven_returns.cumprod()
    return maven_returns


def calculating_signals(maven_inputs, maven_returns):
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
    # calculating rolling volatility and momentum score
    frequency = maven_inputs['frequency'].item()
    if frequency == 'monthly':
        n = 12
        ann = 12
        w_m = 1
    else:
        n = 52
        ann = 13
        w_m = 4
    m = int(maven_inputs['val_period_months'].item() / 12 * n)  # look-back period for valuation
    base = int(maven_inputs['val_period_base'].item() / 12 * n)  # period around look-back point
    vol1 = 0
    vol2 = 0
    mom = 1
    for i in range(0, len(vol_weight)):
        vol1 = vol1 + vol_weight[i] * maven_sqr.shift(i * n).rolling(n).mean()
        vol2 = vol2 + vol_weight[i] * maven_prc.shift(i * n).rolling(n).mean()
    for i in range(0, len(mom_weight)):
        mom = mom * (maven_returns.shift(i * w_m) / maven_returns.shift((i + 1) * w_m)) ** mom_weight[i]
    volatility = n ** 0.5 * (vol1 / sum(vol_weight) - (vol2 / sum(vol_weight)) ** 2) ** 0.5
    momentum = (mom ** (ann / sum(mom_weight)) - 1) / volatility
    # calculating the value scores
    value = ((maven_returns / maven_returns.shift(int(m - base / 2)).rolling(base).mean()) ** (n / m) - 1) / volatility
    # shorting the dataframes and sorting last observation
    start_date = value.first_valid_index()
    value = value[start_date:]
    momentum = momentum[start_date:]
    n = len(value)
    value_last = value.iloc[n - 1, :]
    momentum_temp = momentum.iloc[n - 1, :].rename('momentum')
    combi_temp = (value_last > long_cutoff) * momentum_temp + (value_last < short_cutoff) * momentum_temp
    combi_temp = combi_temp.rename('value filter')
    momentum_last = pd.concat([momentum_temp, combi_temp], axis=1)
    value_last = value_last.sort_values()
    momentum_last = momentum_last.sort_values(by=['momentum'])
    momentum_last['momentum'] = momentum_last['momentum'] - momentum_last['value filter']
    # determine signals based on a combination of momentum and value scores: value filter results in -999 scores
    temp_value = (value > long_cutoff) * -999
    temp_momentum = (value <= long_cutoff) * momentum
    long_signals = temp_value + temp_momentum
    temp_value = (value < short_cutoff) * -999
    temp_momentum = (value >= short_cutoff) * -momentum
    short_signals = temp_value + temp_momentum
    # ranking signals
    long_signals_rank = long_signals.rank(axis=1, method='first', ascending=False)
    short_signals_rank = short_signals.rank(axis=1, method='first', ascending=False)
    # determining aggregate exposures for mainly the weekly model
    if frequency == 'monthly':
        m = 1
    else:
        m = 4
    long_exposures = long_signals_rank.iloc[n - m: n, :] <= number_signals
    short_exposures = short_signals_rank.iloc[n - m: n, :] <= number_signals
    long_exposures = long_exposures.sum(axis=0)
    short_exposures = short_exposures.sum(axis=0)
    long_exposures = long_exposures[long_exposures != 0]
    short_exposures = short_exposures[short_exposures != 0]
    # filtering and naming top assets
    long_signals_name = pd.DataFrame(np.ones((n, number_signals)), index=value.index)
    short_signals_name = pd.DataFrame(np.ones((n, number_signals)), index=value.index)
    for i in range(0, number_signals):
        long_signals_name.iloc[:, i] = long_signals_rank.apply(lambda x: x[x == i + 1].idxmin(), axis=1)
        short_signals_name.iloc[:, i] = short_signals_rank.apply(lambda x: x[x == i + 1].idxmin(), axis=1)
    return momentum, value, long_signals, short_signals, long_signals_name, short_signals_name, value_last, \
                                                momentum_last, long_exposures, short_exposures, volatility


def run_performance_stats(maven_inputs, asset_inputs, maven_returns, volatility, long_signals, short_signals):
    """
    creating dataframes with maven return series, and benchmarks, asset class exposures and contributions
    :param pd.DataFrame maven_inputs: parameter choices for the model
    :param pd.DataFrame asset_inputs: asset bloomberg tickers
    :param pd.DataFrame maven_returns: formatted return series for maven assets
    :param pd.DataFrame maven_returns: volatility matrix
    :param pd.DataFrame long_signals: asset long signals
    :param pd.DataFrame short_signals: asset short signals
    :return: dataframes with maven return series, asset class exposures and contributions
    """
    # reading inputs and aligning dataframes
    m = len(maven_returns.columns)
    n = len(long_signals)
    number_signals = maven_inputs['number_assets'].item()
    maven_returns = maven_returns.tail(n)
    volatility = volatility.tail(n)
    # determining equal weights and equal volatility weights
    equal_notional = pd.DataFrame((1 / m) * np.ones((n, m)), index=long_signals.index, columns=long_signals.columns)
    equal_risk = ((1 / volatility).T / (1 / volatility).sum(axis=1)).T
    # determining benchmark returns, fully invested across all assets
    returns_en = maven_returns.pct_change() * equal_notional.shift()
    returns_er = maven_returns.pct_change() * equal_risk.shift()
    returns_en.iloc[0, :] = 0
    returns_er.iloc[0, :] = 0
    returns_en_cum = (1 + returns_en.sum(axis=1)).cumprod() * 100
    returns_er_cum = (1 + returns_er.sum(axis=1)).cumprod() * 100
    returns_maven = pd.DataFrame({'equal notional': returns_en_cum, 'equal volatility': returns_er_cum})
    # calculating maven long and short weights
    long_signals_rank = long_signals.rank(axis=1, method='first', ascending=False)
    short_signals_rank = short_signals.rank(axis=1, method='first', ascending=False)
    long_exposures = long_signals_rank <= number_signals
    short_exposures = short_signals_rank <= number_signals
    vol_long = long_exposures * (1 / volatility)
    vol_short = short_exposures * (1 / volatility)
    # capping asset weight to 50%
    equal_risk_long = cap_and_redistribute((vol_long.T / vol_long.sum(axis=1)).T, 0.5)
    equal_risk_short = cap_and_redistribute((vol_short.T / vol_short.sum(axis=1)).T, 0.5)
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
    asset_contribution_long = returns_maven_long.T
    asset_contribution_short = returns_maven_short.T
    asset_contribution_long.index = asset_class
    asset_contribution_short.index = asset_class
    asset_contribution_long = asset_contribution_long.groupby(asset_contribution_long.index).sum().T
    asset_contribution_short = asset_contribution_short.groupby(asset_contribution_short.index).sum().T
    # determining asset class weights
    asset_class_long = equal_risk_long.T
    asset_class_short = equal_risk_short.T
    asset_class_long.index = asset_class
    asset_class_short.index = asset_class
    asset_class_long = asset_class_long.groupby(asset_class_long.index).sum().T
    asset_class_short = asset_class_short.groupby(asset_class_short.index).sum().T
    return returns_maven, asset_class_long, asset_class_short, asset_contribution_long, asset_contribution_short


def cap_and_redistribute(weight_matrix, cap):
    condition = weight_matrix <= cap
    cap_weight = cap * (condition.count(axis=1) - condition.sum(axis=1))
    rest_weight = (weight_matrix * condition).sum(axis=1)
    cap_matrix = weight_matrix.mul((1 - cap_weight) / rest_weight, axis=0).clip(upper=cap)
    return cap_matrix