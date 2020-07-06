"""
Created on Fri Nov  15 17:27:51 2019
ARP
@author: SN69248
"""

import math
import pandas as pd
import numpy as np
import data_etl.data_manipulation as dm


def momentum(index_data, inputs, week_day):
    sig = pd.DataFrame()
    for column in index_data:
        # Calculate intermediate signals
        sig1 = calc_int_mom_signal(column, index_data, inputs, 'sig1')
        sig2 = calc_int_mom_signal(column, index_data, inputs, 'sig2')
        sig3 = calc_int_mom_signal(column, index_data, inputs, 'sig3')
        sig[column] = (sig1 + sig2 + sig3) / 3
        # S-curve cutout for large movement, alternative curve w/out cutoff:sig[column]=2/(1+math.exp(-2*sig[column]))-1
        sig[column] = sig[column] * np.exp(-1 * sig[column].pow(2) / 6) / (math.sqrt(3) * math.exp(-0.5))

    sig = dm.set_data_frequency(sig, inputs['frequency'].item(), week_day)
    sig = sig.shift(inputs['time_lag'].item(), freq="D")
    return sig


def calc_int_mom_signal(column, index_data, inputs, signal_name):
    sig_i = (index_data[column].ewm(alpha=2 / inputs[f'{signal_name}_short'].item()).mean()
             / index_data[column].ewm(alpha=2 / inputs[f'{signal_name}_long'].item()).mean() - 1)
    # Normalise signal
    sig_i = sig_i/sig_i.rolling(window=inputs['volatility_window'].item()).std()
    return sig_i

def mom (data, weights):
    """

    :param data: data to apply the momentum calcs to
    :param weights: weights  to apply, in a list  of variable length
    :return: DataFrame of the momentum scores. The first item in the weights list is applied to the most recent observation as an exponential weight, then etc.
    """
    # this wont change the frequency of data
    # variable number of inputs (weights)
    # ensure that lag 1 weight is first, i.e. most recent first.
    mom = pd.DataFrame([], columns = data.columns)
    denominator = 0
    for i in list(range(0,len(weights))):
        if i == 0:
            mom = weights[i] * data
            denominator = weights[i]
        else:
            mom = mom + weights[i] * data.shift(i)
            denominator = denominator + weights[i]
    x = mom/denominator
    return x