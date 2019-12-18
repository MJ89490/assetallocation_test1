"""
Created on 12/11/2019
Author: AJ89720
email: Anais.Jeremie@lgim.com
"""

import pytest
import os
from assetallocation_arp.models import times
from assetallocation_arp.data_etl import import_data as gd
import pandas as pd
CURRENT_PATH = os.path.dirname(__file__)

# @pytest.mark.parametrize("original_results, expected_results",
#                          [(os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_for_test", "signals")),
#                            os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", "signals_v_to_test"))),
#                           (os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_for_test", "returns")),
#                            os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", "returns_v_to_test"))),
#                           (os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_for_test", "r")),
#                            os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", "r_v_to_test"))),
#                           (os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_for_test", "positioning")),
#                            os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", "positioning_v_to_test")))])
#
# def test_format_data_and_calc(original_results, expected_results):
#     d_original = pd.read_csv(original_results, index_col=0, sep='\t')
#     d_expected = pd.read_csv(expected_results,  index_col=0, sep='\t')
#     pd.testing.assert_frame_equal(d_original, d_expected, check_names=False, check_column_type=False)

class Data(object):
    def __init__(self, times_inputs, asset_inputs, all_data, signals, returns, r, positioning):
        self.leverage = "v" # to modify in excel
        self.times_inputs = times_inputs
        self.asset_inputs = asset_inputs
        self.all_data = all_data
        self.signals = signals
        self.returns = returns
        self.r = r
        self.positioning = positioning

    def get_data(self):
        self.times_inputs, self.asset_inputs, self.all_data = gd.extract_inputs_and_mat_data("times", None, None)

    def get_times_data(self):
        self.signals, self.returns, self.r, self.positioning = times.format_data_and_calc(self.times_inputs, self.asset_inputs, self.all_data)
        return self.signals

class Test(Data):
    def __init__(self, times_input, asset_inputs, all_data, signals, returns, r, positioning):
        Data.__init__(self, times_input, asset_inputs, all_data, signals, returns, r, positioning)

    def test_format_data_and_calc(self):
        Test.get_data(self)
        signals, returns, r, positioning = Test.get_times_data(self)

        expected_signals = os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", "signals_v_to_test"))
        d_expected = pd.read_csv(expected_signals, index_col=0, sep='\t')
        pd.testing.assert_frame_equal(signals.reset_index(drop=True), d_expected.reset_index(drop=True),
                                      check_column_type=False)
        #return signals, returns, r, positioning

if __name__ == "__main__":
    times_input = pd.DataFrame
    asset_inputs = pd.DataFrame
    all_data = pd.DataFrame
    signals = pd.DataFrame
    returns = pd.DataFrame
    r = pd.DataFrame
    positioning = pd.DataFrame

    obj2 = Test(times_input, asset_inputs, all_data, signals, returns, r, positioning)
    obj2.test_format_data_and_calc()





# @pytest.mark.parametrize("to_test, test",
#                          [("signals_to_test", Data.signals)])
# def test_format_data_and_calc(to_test, test):
#     #change the name of the leverage "v"
#     times_inputs, asset_inputs, all_data = gd.extract_inputs_and_mat_data("times", None, None)
#     signals, returns, r, positioning = times.format_data_and_calc(times_inputs, asset_inputs, all_data)
#
#     print(test)
#     expected_signals = os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", "signals_v_to_test"))
#     d_expected = pd.read_csv(expected_signals, index_col=0, sep='\t')
#     pd.testing.assert_frame_equal(signals.reset_index(drop=True), d_expected.reset_index(drop=True), check_column_type=False)
#
#     expected_returns = os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", "returns_v_to_test"))
#     d_expected = pd.read_csv(expected_returns, index_col=0, sep='\t')
#     pd.testing.assert_frame_equal(returns.reset_index(drop=True), d_expected.reset_index(drop=True), check_column_type=False)
#
#     expected_returns = os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", "r_v_to_test"))
#     d_expected = pd.read_csv(expected_returns, index_col=0, sep='\t')
#     pd.testing.assert_frame_equal(r.reset_index(drop=True), d_expected.reset_index(drop=True), check_column_type=False)
#
#     expected_returns = os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", "positioning_v_to_test"))
#     d_expected = pd.read_csv(expected_returns, index_col=0, sep='\t')
#     pd.testing.assert_frame_equal(positioning.reset_index(drop=True), d_expected.reset_index(drop=True), check_column_type=False)
