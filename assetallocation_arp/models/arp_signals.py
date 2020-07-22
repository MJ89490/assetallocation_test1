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

def momentum_exp (data, observations,ann_freq,exp_indicator):
    """

    :param data: data to apply the momentum calcs to
    :param observations: provide the number of observations required. for example, if 6 is input the weights will then be [6,5,...,1].
    :param ann_freq: becasue we want to annualise these returns, the ann_freq will depend on the frequency of the data - monthly should be 12, weekly 52.
    :param exp_indicator: if present, make weighting exponential
    :return: DataFrame of the momentum scores. The first item in the weights list is applied to the most recent observation as an exponential weight, then etc.
    """
    # this wont change the frequency of data
    # variable number of inputs (weights)
    # ensure that lag 1 weight is first, i.e. most recent first.
    mom = pd.DataFrame([], columns=data.columns)

    if exp_indicator is None:
        weights = list(range(observations, 0, - 1))
    else:
        weights = [a**b for a, b in zip([2] * observations, list(range(observations - 1, - 1, - 1)))]

    for i in list(range(0,len(weights))):
        if i == 0:
            mom = weights[i] * data
        else:
            mom = mom + weights[i] * data.shift(i)
    x = (1 + mom/sum(weights))**ann_freq - 1
    return x