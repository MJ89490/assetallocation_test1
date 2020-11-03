"""
Created on Fri Nov  15 17:27:51 2019
ARP
@author: SN69248
"""
import math

import pandas as pd
import numpy as np

import assetallocation_arp.data_etl.data_manipulation as dm


def momentum(index_data: pd.DataFrame, times: 'Times'):
    sig = pd.DataFrame()
    for col in index_data:
        # Calculate intermediate signals
        # TODO ADD FLOAT BECAURE TYPEERROR BETWEEN FLOAT AND DECIMAL
        sig1 = calc_int_mom_signal(index_data[col], times.short_signals[0], times.long_signals[0], times.volatility_window)
        sig2 = calc_int_mom_signal(index_data[col], times.short_signals[1], times.long_signals[1], times.volatility_window)
        sig3 = calc_int_mom_signal(index_data[col], times.short_signals[2], times.long_signals[2], times.volatility_window)
        sig[col] = (sig1 + sig2 + sig3) / 3
        # S-curve cutout for large movement, alternative curve w/out cutoff:sig[col]=2/(1+math.exp(-2*sig[col]))-1
        sig[col] = sig[col] * np.exp(-1 * sig[col].pow(2) / 6) / (math.sqrt(3) * math.exp(-0.5))

    sig = dm.set_data_frequency(sig, times.frequency, times.day_of_week)
    sig = sig.shift(times.time_lag_in_months, freq="D")
    return sig


def calc_int_mom_signal(index_data: pd.Series, short_signal: float, long_signal: float, volatility_window: int):
    sig_i = (index_data.ewm(alpha=2 / short_signal).mean()
             / index_data.ewm(alpha=2 / long_signal).mean() - 1)
    # Normalise signal
    sig_i = sig_i/sig_i.rolling(window=volatility_window).std()
    return sig_i
