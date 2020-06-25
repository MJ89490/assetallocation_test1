"""
Created on Sun Jun  14 15:47:00 2020
FX Models
@author:
"""

import numpy as np
import pandas as pd
import itertools

from assetallocation_arp.models import portfolio_construction as pc


def format_data(fxmodels_inputs, asset_inputs, all_data):
    """
    creating dataframes with spot and carry indices, cash rates and ppp levels
    :param pd.DataFrame fxmodels_inputs: parameter choices for the models
    :param pd.DataFrame asset_inputs: asset bloomberg tickers
    :param pd.DataFrame all_data: historical bloomberg time series
    :return: dataframes with formatted series for spot and carry indices, cash rates and ppp levels
    """
    # reading inputs
    date_from = fxmodels_inputs['date_from'].item()
    date_to = fxmodels_inputs['date_to'].item()
    all_data = all_data.loc[date_from:date_to]
    all_data = all_data.asfreq('BM')
    fx_list = asset_inputs['currency']
    # determining all crosses and tickers
    fx = [x for x in itertools.combinations(fx_list, 2)]
    spot = [''.join(x) + ' Curncy' for x in fx]
    carry = [''.join(x) + 'CR Curncy' for x in fx]
    # getting spot and carry data for the crosses directly
    spot = all_data[spot]
    spot.columns = spot.columns.str[:6]
    carry = all_data[carry]
    carry.columns = carry.columns.str[:6]
    # deriving ppp and cash rates for the crosses
    ppp = np.array(all_data[asset_inputs['ppp']])
    fx = np.array(list(itertools.combinations(range(ppp.shape[1]), 2))).T
    ppp = ppp[:, fx[1]] / ppp[:, fx[0]]
    ppp = pd.DataFrame(data=ppp, index=carry.index, columns=carry.columns)
    cash = np.array(all_data[asset_inputs['cash_rate']])
    cash = cash[:, fx[0]] - cash[:, fx[1]]
    cash = pd.DataFrame(data=cash, index=carry.index, columns=carry.columns)
    return spot, carry, cash, ppp


def calculate_signals(fxmodels_inputs, spot, carry, cash, ppp):
    """
    creating dataframes with spot and carry indices, cash rates and ppp levels
    :param pd.DataFrame fxmodels_inputs: parameter choices for the models
    :param pd.DataFrame spot: currency spot indices
    :param pd.DataFrame carry: currency carry indices
    :param pd.DataFrame cash: currency cash rates
    :param pd.DataFrame ppp: currency ppp levels
    :return: dataframes with model signals and historical volatility of the currency crosses
    """
    # reading inputs
    signal_type = fxmodels_inputs['signal'].item()
    vol_win = fxmodels_inputs['vol window'].item()
    val_win = fxmodels_inputs['value window'].item()
    base = fxmodels_inputs['historical base'].item()
    mean_rev = fxmodels_inputs['mean reversion'].item()
    base_fx = fxmodels_inputs['currency'].item()
    val_cutoff = fxmodels_inputs['sharpe cutoff'].item()
    resp_func = fxmodels_inputs['response function'].item()
    mom_weight = [fxmodels_inputs['momentum_weight_' + str(x) + 'm'].item() for x in range(1, 7)]
    # calculate rolling volatility and sharpe ratios
    if vol_win is not None:
        volatility = (12 ** 0.5) * carry.pct_change().rolling(vol_win).std()
    else:
        volatility = 1
    if base is None:
        base = 0
    sharpe = (np.log(carry / carry.shift(int(val_win - base / 2)).rolling(base + 1).mean()) + 1) ** (12 / val_win) - 1
    # signal creation for various fx models
    if signal_type == 'momentum':
        mom = 0
        for i in range(0, len(mom_weight)):
            mom = mom + (carry.shift(i) / carry.shift(i + 1) - 1) * mom_weight[i]
        signal = ((1 + mom / sum(mom_weight)) ** 12 - 1) / volatility
    elif signal_type == 'carry':
        signal = cash / volatility
    elif signal_type == 'dynamic hedge':
        signal = (1 / 100)*(cash - ((1 + sharpe) ** (val_win / 12) - 1) * mean_rev) / volatility
    elif signal_type == 'ppp':
        signal = 100 * (ppp.shift(val_win) / spot - 1)
    else:
        signal = 100 * (ppp.shift(val_win) / spot - 1) / mean_rev + cash
    # limited to base currency only yes/no
    if base_fx is not None:
        signal = signal.mul(signal.columns.str.contains(base_fx), axis=1)
    # value cut off yes/no
    if val_cutoff is not None:
        # cond1 = np.sign(signal) == np.sign(sharpe)
        cond1 = np.abs(signal + sharpe) == np.abs(signal) + np.abs(sharpe)
        cond2 = np.abs(sharpe / volatility) > val_cutoff
        signal = (1 - (cond1 & cond2)) * signal
    # response function for momentum signals yes/no
    if resp_func:
        signal = signal * np.exp(-(np.abs(signal) ** 2 / 4))
    # shorting the dataframes
    start_date = signal.first_valid_index()
    signal = signal[start_date:]
    if isinstance(volatility, pd.DataFrame):
        volatility = volatility[start_date:]
    return signal, volatility


def determine_sizing(fxmodels_inputs, asset_inputs, signal, volatility):
    """
    creating dataframes with currency exposures
    :param pd.DataFrame fxmodels_inputs: parameter choices for the models
    :param pd.DataFrame asset_inputs: asset bloomberg tickers
    :param pd.DataFrame signal: model signals
    :param pd.DataFrame volatility: historical volatility of the currency crosses
    :return: dataframes with currency exposures for individual crosses and aggregated
    """
    # reading inputs
    fx_model = fxmodels_inputs['model'].item()
    signal_type = fxmodels_inputs['signal'].item()
    fx_list = asset_inputs['currency']
    top_fx = fxmodels_inputs['top crosses'].item()
    leverage = fxmodels_inputs['exposure'].item()
    # calculating exposures
    if signal_type == 'momentum' or signal_type == 'carry':
        signal_rank = np.abs(signal).rank(axis=1, method='first', ascending=False)
        exposure = (signal_rank <= top_fx) * np.sign(signal).astype(float)
        exposure_vol = np.abs(exposure) * (1 / volatility)
        exposure = np.sign(exposure) * pc.cap_and_redistribute((exposure_vol.T / exposure_vol.sum(axis=1)).T, 0.5)
    elif signal_type == 'ppp':
        signal_rank = np.abs(signal).rank(axis=1, method='first', ascending=False)
        exposure = (signal_rank <= top_fx) * np.sign(signal).astype(float) / top_fx
    else:
        map = create_sizing_mapping()
        exposure = signal.applymap(lambda x: map.index[(x >= map).sum() - 1].item())
        exposure = leverage * exposure * signal.notna().replace(False, np.nan)
    # calculating aggregate exposures per currency
    exposure_agg_strong = pd.DataFrame(index=exposure.index, columns=fx_list)
    exposure_agg_weak = pd.DataFrame(index=exposure.index, columns=fx_list)
    for x in fx_list[:len(fx_list)-1]:
        exposure_agg_strong[x] = exposure.groupby(exposure.columns.str[:3] == x, axis=1).sum()[True].fillna(0)
    for x in fx_list[1:]:
        exposure_agg_weak[x] = exposure.groupby(exposure.columns.str[3:] == x, axis=1).sum()[True]
    exposure_agg = exposure_agg_strong.fillna(0) - exposure_agg_weak.fillna(0)
    return fx_model, exposure, exposure_agg


def create_sizing_mapping():
    map_return = np.append(-1, np.arange(-0.05, 0.055, 0.005)).round(4)
    map_weight = np.append(np.arange(-0.05, 0.005, 0.005), np.arange(0, 0.055, 0.005)).round(4)
    map = pd.DataFrame(data=map_return, index=map_weight)
    return map


def calculate_returns(fxmodels_inputs, carry, signal, exposure, exposure_agg):
    """
    creating dataframes with model returns and currency contributions
    :param pd.DataFrame fxmodels_inputs: parameter choices for the models
    :param pd.DataFrame carry: currency carry indices
    :param pd.DataFrame signal: model signals
    :param pd.DataFrame exposure: currency exposure for individual crosses
    :param pd.DataFrame exposure_agg: currency exposure aggregated
    :return: dataframes with model returns, currency contributions and returns
    """
    # reading inputs
    base_fx = fxmodels_inputs['currency'].item()
    costs = fxmodels_inputs['transaction costs'].item()
    returns = pd.DataFrame(index=exposure.index)
    # return calculations
    returns['returns'] = (exposure.shift() * np.log(carry / carry.shift())).sum(axis=1)
    returns['returns_cum'] = (1 + returns['returns']).cumprod() * 100
    returns['turnover'] = (exposure_agg - exposure_agg.shift()).abs().sum(axis=1) / 2
    transaction_costs = returns['turnover'] * costs / 10000
    returns['returns_net_cum'] = (1 + returns['returns'] - transaction_costs.shift()).cumprod() * 100
    returns['returns_net_cum'][0] = 100
    returns['strength_of_signal'] = (exposure * signal).sum(axis=1)
    # getting return series vs base currency
    carry_base = pd.DataFrame(index=exposure.index, columns=exposure_agg.columns)
    if base_fx is None:
        base_fx = 'USD'
    fx_base = exposure_agg.columns + base_fx
    for x in fx_base:
        if carry.columns.contains(x):
            carry_base[x[:3]] = carry[x]
        elif x == base_fx + base_fx:
            carry_base[base_fx] = 1
        else:
            carry_base[x[:3]] = 1 / carry[base_fx + x[:3]]
    # contribution calculations
    contribution = (exposure_agg.shift() * np.log(carry_base / carry_base.shift())).cumsum()
    return base_fx, returns, contribution, carry_base