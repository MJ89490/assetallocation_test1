"""
Created on Fri Nov  8 17:27:51 2019
DATA MANIPULATION
@author: SN69248
"""

import pandas as pd

from assetallocation_arp.enum import FrequencyTypes as frequency


def set_data_frequency(data, freq, week_day='SUN'):
    # Reduce frequency of a series, used to reflect weekly implementation of a strategy
    if freq == frequency.Frequency.monthly.name:
        data = data.reindex()
        rng = pd.date_range(start=data.index[0], end=data.index[-1], freq='M')
        sig = data.reindex(rng, method='pad')
    elif freq == frequency.Frequency.weekly.name:
        data = data.reindex()
        rng = pd.date_range(start=data.index[0], end=data.index[-1], freq='W-' + week_day)
        sig = data.reindex(rng, method='pad')
    elif freq == frequency.Frequency.daily.name:
        sig = data
    else:
        raise Exception('Frequency not supported')
    return sig



