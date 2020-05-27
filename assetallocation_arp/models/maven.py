"""
Created on Tue May  26 15:58:00 2020
FICA
@author: WK68945 & JF12345
"""

import numpy as np
import pandas as pd
#import data_etl.data_manipulation as dm


def format_data(maven_inputs, asset_inputs, all_data):
    # creating dataframe with index data
    # reading inputs and shortening data
    date_from = maven_inputs['date_from'].item()
    date_to = maven_inputs['date_to'].item()
    frequency = maven_inputs['frequency'].item()
    all_data = all_data.loc[date_from:date_to]
    #
    if frequency == 'monthly':
        all_data = all_data.asfreq('BM')
    else:
        all_data = all_data.asfreq('W-' + maven_inputs['week_day'].item())
    #
    if maven_inputs['er_tr'].item() == 'excess':
        maven_indices = all_data[asset_inputs['bbg_er_ticker']]
    else:
        maven_indices = all_data[asset_inputs['bbg_tr_ticker']]

    return maven_indices
