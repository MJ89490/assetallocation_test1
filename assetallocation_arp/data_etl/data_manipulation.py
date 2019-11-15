"""
Created on Fri Nov  8 17:27:51 2019
DATA MANIPULATION
@author: SN69248
"""

import pandas as pd


def set_data_frequency(data, freq):
    # Reduce frequency of a series, used to reflect weekly implementation of a strategy
    if freq == "monthly":
        data = data.reindex()
        rng = pd.date_range(start=data.index[0], end=data.index[-1], freq='M')
        sig = data.reindex(rng, method='pad')
    elif freq == "weekly":
        data = data.reindex()
        rng = pd.date_range(start=data.index[0], end=data.index[-1], freq='W-MON')
        sig = data.reindex(rng, method='pad')
    elif freq == "daily":
        sig = data
    else:
        raise Exception('Frequency not supported')
    return sig



