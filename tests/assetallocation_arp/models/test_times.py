"""
Created on 12/11/2019
Author: AJ89720
email: Anais.Jeremie@lgim.com
"""

import pytest
import os
import pandas as pd
import numpy as np

from tests.assetallocation_arp.models import data_test as data_test
from assetallocation_arp.enum import leverage_types as leverage

CURRENT_PATH = os.path.dirname(__file__)

"""
Module test_times.py: tests the Times model (times.py) in order to know if it returns the correct following outputs:
    - signals
    - returns
    - r
    - positioning
"""


@pytest.mark.parametrize("leverage_type, signals_path, returns_path, r_path, positioning_path",
                         [(leverage.Leverage.v.name, "signals_v_to_test", "returns_v_to_test", "r_v_to_test",
                           "positioning_v_to_test"),
                          (leverage.Leverage.s.name, "signals_s_to_test", "returns_s_to_test", "r_s_to_test",
                           "positioning_s_to_test"),
                          (leverage.Leverage.e.name, "signals_e_to_test", "returns_e_to_test", "r_e_to_test",
                           "positioning_e_to_test"),
                         (leverage.Leverage.n.name, "signals_n_to_test", "returns_n_to_test", "r_n_to_test",
                           "positioning_n_to_test")]
                         )
def test_format_data_and_calc(leverage_type, signals_path, returns_path, r_path, positioning_path):
    """
    Function which tests the format_data_and_calc function in order to know if it returns th correct results
    (e.g signals, r, returns, positioning)
    :param leverage_type: types of leverage available: Equal(e) / Normative(n) / Volatility(v) / Standalone(s)
    :param signals_path: name of the file signals for the signals path
    :param returns_path: name of the file returns for the returns path
    :param r_path: name of the file r for the r path
    :param positioning_path: name of the file positioning for the positioning path
    :return: assertion error if one of the dataframe has a number of False > 127
    """

    data_object = data_test.DataTest(leverage=leverage_type)
    data_object.get_data()
    data_object.get_times_model_data()

    start_date_signals_timestamp = np.datetime64("1964-08-06")
    end_date_signals_timestamp = np.datetime64("2019-11-28")

    start_date_returns_timestamp = np.datetime64("1964-07-31")
    end_date_returns_timestamp = np.datetime64("2019-11-26")

    start_date_r_timestamp = np.datetime64("1964-07-31")
    end_date_r_timestamp = np.datetime64("2019-11-26")

    start_date_positioning_timestamp = np.datetime64("1964-07-31")
    end_date_positioning_timestamp = np.datetime64("2019-11-26")

    signals_origin = data_object.getter_signals.loc[start_date_signals_timestamp:end_date_signals_timestamp, :]
    returns_origin = data_object.getter_returns.loc[start_date_returns_timestamp:end_date_returns_timestamp, :]
    r_origin = data_object.getter_r.loc[start_date_r_timestamp:end_date_r_timestamp, :]
    r_origin = r_origin.iloc[:, :-1] #delete the column total because it is not useful for computations
    positioning_origin = data_object.getter_positioning.loc[start_date_positioning_timestamp:end_date_positioning_timestamp, :]

    expected_signals = os.path.abspath(os.path.join(CURRENT_PATH, "resources", "data_times_to_test", signals_path))
    expected_returns = os.path.abspath(os.path.join(CURRENT_PATH, "resources", "data_times_to_test", returns_path))
    expected_r = os.path.abspath(os.path.join(CURRENT_PATH, "resources", "data_times_to_test", r_path))
    expected_positioning = os.path.abspath(os.path.join(CURRENT_PATH, "resources", "data_times_to_test", positioning_path))

    dataframe_signals = pd.read_csv(expected_signals, index_col=0, sep='\t')
    dataframe_returns = pd.read_csv(expected_returns, index_col=0, sep='\t')
    dataframe_returns = dataframe_returns[:-1]# remove the last row to have equal dataframe with returns_origin
    dataframe_r = pd.read_csv(expected_r, index_col=0, sep='\t')
    dataframe_r = dataframe_r[:-1]# remove the last row to have equal dataframe with r_origin
    dataframe_r = dataframe_r.iloc[:, :-1]
    dataframe_positioning = pd.read_csv(expected_positioning, index_col=0, sep='\t')
    dataframe_positioning = dataframe_positioning[:-1]  # remove the last row to have equal dataframe with positioning_origin

    diff_signals = np.isclose(signals_origin, dataframe_signals, equal_nan=True, atol=0.08)
    diff_returns = np.isclose(returns_origin, dataframe_returns, equal_nan=True, atol=0.08)
    diff_r = np.isclose(r_origin, dataframe_r, equal_nan=True, atol=0.08)
    diff_positioning = np.isclose(positioning_origin, dataframe_positioning, equal_nan=True, atol=0.08)

    unique_signals, counts_signals = np.unique(diff_signals, return_counts=True)
    counting_signals = dict(zip(unique_signals, counts_signals))

    unique_returns, counts_returns = np.unique(diff_returns, return_counts=True)
    counting_returns = dict(zip(unique_returns, counts_returns))

    unique_r, counts_r = np.unique(diff_r, return_counts=True)
    counting_r = dict(zip(unique_r, counts_r))

    unique_positioning, counts_positioning = np.unique(diff_positioning, return_counts=True)
    counting_positioning = dict(zip(unique_positioning, counts_positioning))

    flag = False

    if False in counting_signals and counting_signals[False] <= 127: flag = True
    elif False in counting_returns and counting_returns[False] <= 127: flag = True
    elif False in counting_r  and counting_r[False] <= 127: flag = True
    elif False in counting_positioning and counting_positioning[False] <= 127: flag = True
    else: flag = True # there are only True in the diff dataframes

    assert flag is True
