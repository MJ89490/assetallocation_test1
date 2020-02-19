import numpy as np
import pandas as pd

from assetallocation_arp.models import portfolio_construction as pc
from assetallocation_arp.models import arp_signals as arp
from pandas.tseries.offsets import BDay
from assetallocation_arp.enum import leverage_types as leverage_name

def format_data_and_calc(effect_inputs, asset_inputs, all_data):
    # format data and inputs
    asset_inputs_t = asset_inputs.set_index('asset').T
    effect_data = all_data[asset_inputs.signal_ticker]


    # return signals, returns, r, positioning