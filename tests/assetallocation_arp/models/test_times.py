"""
Created on 12/11/2019
Author: AJ89720
email: Anais.Jeremie@lgim.com
"""

import pytest
import os
import pandas as pd

from tests.assetallocation_arp.models import data_test as data_test
from assetallocation_arp.enum import leverage_types as leverage

CURRENT_PATH = os.path.dirname(__file__)

"""
Module test_times.py: tests the Times model (data_times_old.py) in order to know if it returns the correct following outputs:
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
    :return: assertion error if the two compared dataframes are not equal
    """

    data_object = data_test.DataTest(leverage=leverage_type)
    data_object.get_data()
    data_object.get_times_model_data()

    signals_origin = data_object.getter_signals
    returns_origin = data_object.getter_returns
    r_origin = data_object.getter_r
    positioning_origin = data_object.getter_positioning

    expected_signals = os.path.abspath(os.path.join(CURRENT_PATH, "resources", "data_times_to_test", signals_path))
    expected_returns = os.path.abspath(os.path.join(CURRENT_PATH, "resources", "data_times_to_test", returns_path))
    expected_r = os.path.abspath(os.path.join(CURRENT_PATH, "resources", "data_times_to_test", r_path))
    expected_positioning = os.path.abspath(os.path.join(CURRENT_PATH, "resources", "data_times_to_test", positioning_path))

    dataframe_signals = pd.read_csv(expected_signals, index_col=0, sep='\t')
    dataframe_returns = pd.read_csv(expected_returns, index_col=0, sep='\t')
    dataframe_r = pd.read_csv(expected_r, index_col=0, sep='\t')
    dataframe_positioning = pd.read_csv(expected_positioning, index_col=0, sep='\t')

    pd.testing.assert_frame_equal(signals_origin.reset_index(drop=True),
                                      dataframe_signals.reset_index(drop=True), check_column_type=False)
    pd.testing.assert_frame_equal(returns_origin.reset_index(drop=True),
                                      dataframe_returns.reset_index(drop=True), check_column_type=False)
    pd.testing.assert_frame_equal(r_origin.reset_index(drop=True),
                                      dataframe_r.reset_index(drop=True), check_column_type=False)
    pd.testing.assert_frame_equal(positioning_origin.reset_index(drop=True),
                                      dataframe_positioning.reset_index(drop=True), check_column_type=False)


