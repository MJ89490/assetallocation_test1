"""
Created on Fri Nov  15 17:27:51 2019
ARP
@author: SN69248
"""

import math
import pandas as pd
import numpy as np
import data_etl.data_manipulation as dm


def momentum(index_data, inputs):
    sig = pd.DataFrame()
    for column in index_data:
        sig1 = index_data[column].ewm(alpha=2 / inputs['sig1_short'].item()).mean() / index_data[column].ewm(alpha=2 / inputs['sig1_long'].item()).mean() - 1
        sig2 = index_data[column].ewm(alpha=2 / inputs['sig2_short'].item()).mean() / index_data[column].ewm(alpha=2 / inputs['sig2_long'].item()).mean() - 1
        sig3 = index_data[column].ewm(alpha=2 / inputs['sig3_short'].item()).mean() / index_data[column].ewm(alpha=2 / inputs['sig3_long'].item()).mean() - 1

        sig[column] = (sig1 / sig1.rolling(window=inputs['volatility_window'].item()).std() + sig2 /
                       sig2.rolling(window=inputs['volatility_window'].item()).std() + sig3 / sig3.rolling(window=inputs['volatility_window'].item()).std()) / 3

    # S-curve cut out for large movement, alternative curve without cutoff: sig[column]=2/(1+math.exp(-2*sig[column]))-1
        sig[column] = sig[column] * np.exp(-1 * sig[column].pow(2) / 6) / (math.sqrt(3) * math.exp(-0.5))

    sig = dm.set_data_frequency(sig, inputs['frequency'].item())
    sig = sig.shift(inputs['time_lag'].item(), freq="D")
    return sig
