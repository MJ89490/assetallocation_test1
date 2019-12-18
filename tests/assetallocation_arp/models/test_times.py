"""
Created on 12/11/2019
Author: AJ89720
email: Anais.Jeremie@lgim.com
"""

import pytest
import os
import mock
from assetallocation_arp.models import times
from assetallocation_arp.data_etl import import_data as gd
import pandas as pd
CURRENT_PATH = os.path.dirname(__file__)


# @pytest.mark.parametrize("data_object,"
#                          "signals_v_path, returns_v_path, r_v_path, positioning_v_path, "
#                          "signals_s_path, returns_s_path, r_s_path, positioning_s_path,"
#                          "signals_e_path, returns_e_path, r_e_path, positioning_e_path ",
#                          "signals_n_path, returns_n_path, r_n_path, positioning_n_path ",
#                          [(Data(leverage="v", times_inputs=pd.DataFrame, asset_inputs=pd.DataFrame,
#                                 all_data=pd.DataFrame,
#                                 signals=pd.DataFrame, returns=pd.DataFrame, r=pd.DataFrame, positioning=pd.DataFrame),
#                            os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", "signals_v_to_test")),
#                            os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", "returns_v_to_test")),
#                            os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", "r_v_to_test")),
#                            os.path.abspath(
#                                os.path.join(CURRENT_PATH, "..", "data_times_to_test", "positioning_v_to_test"))
#
#                            )])

# os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", "signals_v_to_test")),
#                            os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", "returns_v_to_test")),
#                            os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", "r_v_to_test")),
#                            os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", "positioning_v_to_test")))])
                       #    (Data(leverage="s", times_inputs=pd.DataFrame, asset_inputs=pd.DataFrame, all_data=pd.DataFrame,
                       # signals=pd.DataFrame, returns=pd.DataFrame, r=pd.DataFrame, positioning=pd.DataFrame), "PUT PATH LEVERAGE"),
                       #    (Data(leverage="e", times_inputs=pd.DataFrame, asset_inputs=pd.DataFrame, all_data=pd.DataFrame,
                       # signals=pd.DataFrame, returns=pd.DataFrame, r=pd.DataFrame, positioning=pd.DataFrame), "PUT PATH LEVERAGE"),
                       #    (Data(leverage="n", times_inputs=pd.DataFrame, asset_inputs=pd.DataFrame, all_data=pd.DataFrame,
                       # signals=pd.DataFrame, returns=pd.DataFrame, r=pd.DataFrame, positioning=pd.DataFrame), "PUT PATH LEVERAGE")
                       #    ])

class Data:
    def __init__(self, leverage, times_inputs, asset_inputs, all_data, signals, returns, r, positioning):
        self.leverage = leverage # to modify in excel
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
        return self.signals, self.returns, self.r, self.positioning

#A TRANSFORMER EN FIXTURE?????? TROP DE PARAMETRES DANS PARAMETRIZE NON LISBLE APRES
# @pytest.fixture()
# def expected_signal():
#     df = pd.read_csv
#     df.colu
#     return df

@pytest.mark.parametrize("data_object, signals_v_path, returns_v_path, r_v_path, positioning_v_path",
                         [(Data(leverage="v", times_inputs=pd.DataFrame, asset_inputs=pd.DataFrame, all_data=pd.DataFrame, signals=pd.DataFrame, returns=pd.DataFrame, r=pd.DataFrame, positioning=pd.DataFrame),
                           os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", "signals_v_to_test")),os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", "returns_v_to_test")),
                           os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", "r_v_to_test")),os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", "positioning_v_to_test")))
                         ])
def test_format_data_and_calc(data_object, signals_v_path, returns_v_path, r_v_path, positioning_v_path):

        # data_object = Data(times_inputs=pd.DataFrame, asset_inputs=pd.DataFrame, all_data=pd.DataFrame, signals=pd.DataFrame, returns=pd.DataFrame, r=pd.DataFrame, positioning=pd.DataFrame)
        data_object.get_data()
        signals_origin, returns_origin, r_origin, positioning_origin = data_object.get_times_data()

        # expected_signals = os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", "signals_v_to_test"))
        # expected_returns = os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", "returns_v_to_test"))
        # expected_r = os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", "r_v_to_test"))
        # expected_positioning = os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", "positioning_v_to_test"))

        expected_signals = signals_v_path
        expected_returns = returns_v_path
        expected_r = r_v_path
        expected_positioning = positioning_v_path
  
        #expected_output = anais_function()
        dataframe_signals = pd.read_csv(expected_signals, index_col=0, sep='\t')
        dataframe_returns = pd.read_csv(expected_returns, index_col=0, sep='\t')
        dataframe_r = pd.read_csv(expected_r, index_col=0, sep='\t')
        dataframe_positioning = pd.read_csv(expected_positioning, index_col=0, sep='\t')

        pd.testing.assert_frame_equal(signals_origin.reset_index(drop=True), dataframe_signals.reset_index(drop=True), check_column_type=False)
        pd.testing.assert_frame_equal(returns_origin.reset_index(drop=True), dataframe_returns.reset_index(drop=True), check_column_type=False)
        pd.testing.assert_frame_equal(r_origin.reset_index(drop=True), dataframe_r.reset_index(drop=True), check_column_type=False)
        pd.testing.assert_frame_equal(positioning_origin.reset_index(drop=True), dataframe_positioning.reset_index(drop=True), check_column_type=False)



