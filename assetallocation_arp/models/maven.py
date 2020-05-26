"""
Created on Tue May  26 15:58:00 2020
FICA
@author: WK68945 & JF12345
"""

import numpy as np
import pandas as pd
import data_etl.data_manipulation as dm


def format_data(maven_inputs, asset_inputs, all_data):
    # creating dataframe with index data
    # reading inputs and shortening data
    asset = asset_inputs['asset']
    date_from = maven_inputs['date_from'].item()
    date_to = maven_inputs['date_to'].item()
    all_data = all_data.loc[date_from:date_to]
    all_data = dm.set_data_frequency(all_data, maven_inputs['frequency'].item(), maven_inputs['week_day'].item())
    #
    if maven_inputs['excess_totalreturn'].item() == 'excess':
        maven_indices = all_data[asset_inputs['bbg_er_ticker']]
    else:
        maven_indices = all_data[asset_inputs['bbg_tr_ticker']]

    return maven_indices
