"""
Created on Fri Nov  15 17:27:51 2019
TIMES
@author: SN69248
"""

import numpy as np

import data_etl.import_data as gd
import models.portfolio_construction as pc
import models.arp as arp

def extract_inputs_from_mat_file(mat_file = None, input_file = None):

    if mat_file is None:
        file_path = r'H:\assetallocation_arp\data\raw\matlabData.mat'
    else:
        file_path = mat_file

    if input_file is None:
        input_path = r'H:\assetallocation_arp\data\raw\ARP_Model_Inputs.xlsx'
    else:
        input_path = input_file

    # load data and inputs
    times_inputs = gd.data_frame_from_xlsx(input_path, 'rng_times_inputs', 1)
    asset_inputs = gd.data_frame_from_xlsx(input_path, 'rng_times_assets', 1)
    all_data = gd.matfile_to_dataframe(file_path)
    return (times_inputs, asset_inputs, all_data)


def format_data_and_calc(times_inputs, asset_inputs, all_data):
    # format data and inputs
    asset_inputs_t = asset_inputs.set_index('asset').T
    #
    all_data = all_data[all_data.index.dayofweek < 5]  # remove weekends
    times_data = all_data[asset_inputs.signal_ticker]
    futures_data = all_data[asset_inputs.future_ticker].pct_change()
    times_data.columns = asset_inputs.asset
    futures_data.columns = asset_inputs.asset
    #
    costs = asset_inputs_t.loc['costs']
    leverage = asset_inputs_t.loc['leverage']
    leverage_type = times_inputs['leverage_type'].item()

    # calculate signals
    signals = arp.momentum(times_data, times_inputs, times_inputs['week_day'].item())

    # apply leverage
    leverage_data = pc.apply_leverage(futures_data, leverage_type, leverage)
    leverage_data[leverage.index[leverage.isnull()]] = np.nan
    leverage_data = leverage_data.shift(periods=times_inputs['time_lag'].item(), freq='D', axis=0).reindex(futures_data.append(signals.iloc[-1]).index, method='pad')

    # calculate leveraged positions and returns
    if leverage_type == 's':
        (returns, r, positioning) = pc.return_ts(signals, futures_data, leverage_data, costs, 0)
    else:
        (returns, r, positioning) = pc.return_ts(signals, futures_data, leverage_data, costs, 1)
        (returns, r, positioning) = pc.rescale(returns, r, positioning, "Total", 0.01)


def run_model(model_type, mat_file, input_file):
    if model_type == "times":
        times_inputs, asset_inputs, all_data = extract_inputs_from_mat_file(mat_file, input_file)
        format_data_and_calc(times_inputs, asset_inputs, all_data)

if __name__ == "__main__":
    run_model("times")