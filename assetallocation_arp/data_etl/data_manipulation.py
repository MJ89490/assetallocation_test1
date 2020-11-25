"""
Created on Fri Nov  8 17:27:51 2019
DATA MANIPULATION
@author: SN69248
"""

import pandas as pd

from assetallocation_arp.common_libraries import frequency_types as frequency


def set_data_frequency(data, freq, week_day, calculation_type='na'):
    # Reduce frequency of a series, used to reflect weekly implementation of a strategy
    # TODO CHANGE IT LATER
    if not isinstance(freq, str):
        f = {'weekly': 'weekly', 'monthly': 'monthly', 'daily': 'daily'}
        freq = f[freq.name]

    if not isinstance(week_day, str):
        w = {'MON': 'MON', 'TUE': 'TUE', 'WED': 'WED', 'THU': 'THU', 'FRI': 'FRI'}
        week_day = w[week_day.name]

    if freq == frequency.Frequency.monthly.name:
        data = data.reindex()
        if calculation_type == 'average':
            sig = data.resample('M').mean()
        else:
            rng = pd.date_range(start=data.index[0], end=data.index[-1], freq='M')
            sig = data.reindex(rng, method='pad')
    elif freq == frequency.Frequency.weekly.name:
        data = data.reindex()
        if calculation_type == 'average':
            sig = data.resample('W-' + week_day).mean()
        else:
            rng = pd.date_range(start=data.index[0], end=data.index[-1], freq='W-' + week_day)
            sig = data.reindex(rng, method='pad')
    elif freq == frequency.Frequency.daily.name:
        sig = data
    else:
        raise Exception('Frequency not supported')
    return sig



