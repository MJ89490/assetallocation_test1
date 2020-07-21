"""
Created on Fri Nov  15 17:27:51 2019
TIMES
@author: SN69248
"""

import numpy as np
import pandas as pd

from assetallocation_arp.models import portfolio_construction as pc
from assetallocation_arp.models import arp_signals as arp
from pandas.tseries.offsets import BDay
from assetallocation_arp.common_libraries import leverage_types as leverage_name


def format_data_and_calc(times_inputs, asset_inputs, all_data):

    # format data and inputs
    asset_inputs_t = asset_inputs.set_index('asset').T
    all_data = all_data[ all_data.index.values > np.datetime64(times_inputs['DateFrom'].item())]
    times_data = all_data[asset_inputs.signal_ticker]
    futures_data = all_data[asset_inputs.future_ticker].pct_change()
    times_data.columns = asset_inputs.asset
    futures_data.columns = asset_inputs.asset
    #
    costs = asset_inputs_t.loc['costs']
    leverage = asset_inputs_t.loc['s_leverage']
    leverage_type = times_inputs['leverage_type'].item()

    # calculate signals
    signals = arp.momentum(times_data, times_inputs, times_inputs['week_day'].item())
    # apply leverage
    leverage_data = pc.apply_leverage(futures_data, leverage_type, leverage)
    leverage_data[leverage.index[leverage.isnull()]] = np.nan
    index_df = futures_data.append(pd.DataFrame(index=futures_data.iloc[[-1]].index + BDay(2)), sort=True).index
    leverage_data = leverage_data.shift(periods=times_inputs['time_lag'].item(), freq='D', axis=0).reindex(
        index_df, method='pad')
    # calculate leveraged positions and returns
    if leverage_type == leverage_name.Leverage.s.name:
        (returns, r, positioning) = pc.return_ts(signals, futures_data, leverage_data, costs, 0)
    else:
        (returns, r, positioning) = pc.return_ts(signals, futures_data, leverage_data, costs, 1)
        (returns, r, positioning) = pc.rescale(returns, r, positioning, "Total", 0.01)
    return signals, returns, r, positioning







