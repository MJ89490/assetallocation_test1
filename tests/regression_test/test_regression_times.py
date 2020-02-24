"""
Created on 17/02/2020
Author: AJ89720
email: Anais.Jeremie@lgim.com
"""

import pytest
import os
import pandas as pd

CURRENT_PATH = os.path.dirname(__file__)

"""
Module test_regression_times.py: tests the Times model (times.py) and the old model results in order to know 
if they return the correct following outputs:
    - signals
    - returns
    - r
    - positioning
"""


# @pytest.mark.parametrize("signals_new, signals_old, ret1_new, ret1_old, R1_new, R1_old, positioning_new, positioning_old",
#                          [("signals_new_v", "signals_old_v", "ret1_new_v", "ret1_old_v", "R1_new_v", "R1_old_v",
#                            "positioning_new_v", "positioning_old_v")])
@pytest.mark.parametrize("signals_new, signals_old, ret1_new, ret1_old, R1_new, R1_old, positioning_new, positioning_old",
                         [("signals_new_e", "signals_old_e", "ret1_new_e", "ret1_old_e", "R1_new_e", "R1_old_e",
                           "positioning_new_e", "positioning_old_e"),
                          ("signals_new_n", "signals_old_n", "ret1_new_n", "ret1_old_n", "R1_new_n", "R1_old_n",
                           "positioning_new_n", "positioning_old_n"),
                          ("signals_new_v", "signals_old_v", "ret1_new_v", "ret1_old_v", "R1_new_v", "R1_old_v",
                           "positioning_new_v", "positioning_old_v"),
                          ("signals_new_s", "signals_old_s", "ret1_new_s", "ret1_old_s", "R1_new_s", "R1_old_s",
                           "positioning_new_s", "positioning_old_s")
                          ])
def test_compare_times_models(signals_new, signals_old, ret1_new, ret1_old, R1_new, R1_old, positioning_new, positioning_old):

    signals_new = os.path.abspath(os.path.join(CURRENT_PATH, "..", "regression_test", "resources", signals_new))
    signals_old = os.path.abspath(os.path.join(CURRENT_PATH, "..", "regression_test", "resources", signals_old))

    ret1_new = os.path.abspath(os.path.join(CURRENT_PATH, "..", "regression_test", "resources", ret1_new))
    ret1_old = os.path.abspath(os.path.join(CURRENT_PATH, "..", "regression_test", "resources", ret1_old))

    R1_new = os.path.abspath(os.path.join(CURRENT_PATH, "..", "regression_test", "resources", R1_new))
    R1_old = os.path.abspath(os.path.join(CURRENT_PATH, "..", "regression_test", "resources", R1_old))

    positioning_new = os.path.abspath(os.path.join(CURRENT_PATH, "..", "regression_test", "resources", positioning_new))
    positioning_old = os.path.abspath(os.path.join(CURRENT_PATH, "..", "regression_test", "resources", positioning_old))

    dataframe_R1_new = pd.read_csv(R1_new, index_col=0, sep='\t')
    dataframe_R1_old = pd.read_csv(R1_old, index_col=0, sep='\t')

    dataframe_ret1_new = pd.read_csv(ret1_new, index_col=0, sep='\t')
    dataframe_ret1_old = pd.read_csv(ret1_old, index_col=0, sep='\t')

    dataframe_positioning_new = pd.read_csv(positioning_new, index_col=0, sep='\t')
    dataframe_positioning_old = pd.read_csv(positioning_old, index_col=0, sep='\t')

    dataframe_signals_new = pd.read_csv(signals_new, index_col=0, sep='\t')
    dataframe_signals_old = pd.read_csv(signals_old, index_col=0, sep='\t')

    pd.testing.assert_frame_equal(dataframe_signals_new.reset_index(drop=True),
                                  dataframe_signals_old.reset_index(drop=True), check_column_type=False)
    pd.testing.assert_frame_equal(dataframe_R1_new.reset_index(drop=True),
                                  dataframe_R1_old.reset_index(drop=True), check_column_type=False)
    pd.testing.assert_frame_equal(dataframe_ret1_new.reset_index(drop=True),
                                  dataframe_ret1_old.reset_index(drop=True), check_column_type=False)
    pd.testing.assert_frame_equal(dataframe_positioning_new.reset_index(drop=True),
                                  dataframe_positioning_old.reset_index(drop=True), check_column_type=False)




