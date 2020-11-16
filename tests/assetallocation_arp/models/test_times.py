"""
Created on 12/11/2019
Author: AJ89720
email: Anais.Jeremie@lgim.com
"""

import pytest
import os
import pandas as pd

from assetallocation_arp.models.times import format_data_and_calc
from common_libraries.dal_enums.strategy import Leverage

CURRENT_PATH = os.path.dirname(__file__)

"""
Module test_times.py: tests the Times model (times.py) in order to know if it returns the correct following outputs:
    - signals
    - returns
    - r
    - positioning
"""


@pytest.mark.parametrize("leverage_type, signals_output, returns_output, positioning_output, r_output",
                         [(Leverage.v.name, "signals_leverage_v", "returns_leverage_v", "positioning_leverage_v", "r_leverage_v"),
                          (Leverage.e.name, "signals_leverage_e", "returns_leverage_e", "positioning_leverage_e", "r_leverage_e"),
                          (Leverage.n.name, "signals_leverage_n", "returns_leverage_n", "positioning_leverage_n", "r_leverage_n"),
                          (Leverage.s.name, "signals_leverage_s", "returns_leverage_s", "positioning_leverage_s", "r_leverage_s")]
                         )
def test_format_data_and_calc(leverage_type, signals_output, returns_output, positioning_output, r_output):
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

    times_inputs_data = f'times_inputs_leverage_{leverage_type}'
    times_inputs = pd.read_csv(os.path.abspath(os.path.join(CURRENT_PATH, "resources", "times", "inputs_leverages_origin",
                                                            times_inputs_data)), index_col=0)

    asset_inputs_data = pd.read_csv(os.path.abspath(os.path.join(CURRENT_PATH, "resources", "times", "inputs_leverages_origin",
                                                                 "asset_input")), index_col=0)

    all_data = pd.read_csv(os.path.abspath(os.path.join(CURRENT_PATH, "resources", "times", "inputs_leverages_origin",
                                                        "all_data")), index_col=0)

    index_all_data = [pd.Timestamp(date) for date in all_data.index.values]

    all_data = all_data.reindex(index_all_data)# reset the dates of the index to Timestamp

    signals_origin, returns_origin, r_origin, positioning_origin = format_data_and_calc(times_inputs=times_inputs,
                                                                                        asset_inputs=asset_inputs_data,
                                                                                        all_data=all_data)

    signals = pd.read_csv(os.path.abspath(os.path.join(CURRENT_PATH, "resources", "times", "outputs_leverages_to_test",
                                                       signals_output)), index_col=0)
    returns = pd.read_csv(os.path.abspath(os.path.join(CURRENT_PATH, "resources", "times", "outputs_leverages_to_test",
                                                       returns_output)), index_col=0)
    positioning = pd.read_csv(os.path.abspath(os.path.join(CURRENT_PATH, "resources", "times", "outputs_leverages_to_test",
                                                           positioning_output)), index_col=0)
    r = pd.read_csv(os.path.abspath(os.path.join(CURRENT_PATH, "resources", "times", "outputs_leverages_to_test",
                                                 r_output)), index_col=0)

    pd.testing.assert_frame_equal(signals_origin.reset_index(drop=True),
                                  signals.reset_index(drop=True), check_column_type=False)
    pd.testing.assert_frame_equal(returns_origin.reset_index(drop=True),
                                  returns.reset_index(drop=True), check_column_type=False)
    pd.testing.assert_frame_equal(positioning_origin.reset_index(drop=True),
                                  positioning.reset_index(drop=True), check_column_type=False)
    pd.testing.assert_frame_equal(r_origin.reset_index(drop=True),
                                  r.reset_index(drop=True), check_column_type=False)

