"""
Created on Fri Nov  15 17:27:51 2019
TIMES
@author: SN69248
"""

import numpy as np

import models.portfolio_construction as pc
import models.arp_signals as arp
import pandas as pd
from pandas.tseries.offsets import BDay


def format_data_and_calc(times_inputs, asset_inputs, all_data):
    # format data and inputs
    asset_inputs_t = asset_inputs.set_index('asset').T                              #True: from the data
    #
    times_data = all_data[asset_inputs.signal_ticker]                               #True: from the data
    futures_data = all_data[asset_inputs.future_ticker].pct_change()                #True: from the data
    times_data.columns = asset_inputs.asset                                         #True: from the data
    futures_data.columns = asset_inputs.asset                                       #True: from the data
    #
    costs = asset_inputs_t.loc['costs']                                             #True: from the data
    leverage = asset_inputs_t.loc['s_leverage']                                     #True: from the data
    leverage_type = times_inputs['leverage_type'].item()                            #True: from the data

    # calculate signals
    signals = arp.momentum(times_data, times_inputs, times_inputs['week_day'].item()) #False

    # apply leverage
    leverage_data = pc.apply_leverage(futures_data, leverage_type, leverage)
    leverage_data[leverage.index[leverage.isnull()]] = np.nan
    index_df = futures_data.append(pd.DataFrame(index=futures_data.iloc[[-1]].index + BDay(2)), sort=True).index
    leverage_data = leverage_data.shift(periods=times_inputs['time_lag'].item(), freq='D', axis=0).reindex(
        index_df, method='pad')

    # calculate leveraged positions and returns
    if leverage_type == 's':
        (returns, r, positioning) = pc.return_ts(signals, futures_data, leverage_data, costs, 0)    #False
    else:
        (returns, r, positioning) = pc.return_ts(signals, futures_data, leverage_data, costs, 1)    #False
        (returns, r, positioning) = pc.rescale(returns, r, positioning, "Total", 0.01)              #False
    return signals, returns, r, positioning




