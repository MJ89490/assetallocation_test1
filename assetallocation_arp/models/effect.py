import numpy as np
import pandas as pd

from assetallocation_arp.models import portfolio_construction as pc
from assetallocation_arp.models import arp_signals as arp
from pandas.tseries.offsets import BDay
from assetallocation_arp.enum import leverage_types as leverage_name

def format_data_and_calc(effect_inputs, asset_inputs, all_data):
    # format data and inputs

    asset_inputs_t = asset_inputs.set_index('asset').T
    # times_data = all_data[asset_inputs.signal_ticker]
    l = asset_inputs.spot_ticker
    effect_spot_data = all_data[asset_inputs.spot_ticker]
    effect_data = all_data[asset_inputs.strategy_inputs]


    trend_type = asset_inputs_t.loc['trend_indicator']

    # futures_data = all_data[asset_inputs.(trend_type)'_ticker'].pct_c+hange()

    if trend_type == 'carry':
        col = 'carry_ticker'
    else:
        col = 'spot_ticker'

    futures_data = all_data[asset_inputs.loc[col]].pct_change()

    short_ma = asset_inputs_t.loc['short_ma']
    long_ma = asset_inputs_t.loc['long_ma']

    costs = np.divide(asset_inputs_t.loc['spread_bps'],100)
