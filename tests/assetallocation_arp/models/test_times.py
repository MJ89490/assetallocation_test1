"""
Created on 12/11/2019
Author: AJ89720
email: Anais.Jeremie@lgim.com
"""

import pytest
import os
import pandas as pd
import enum


CURRENT_PATH = os.path.dirname(__file__)
INPUT_FILE = os.path.abspath(os.path.join(CURRENT_PATH, "arp_dashboard _test_copy.xlsm"))

# Equal(e) / Normative(n) / Volatility(v) / Standalone(s)

class Models(enum.Enum):
    times = 0
    maven = 1
    effect = 2
    curp = 3
    fica = 4
    factor = 5
    comca = 6

class LeverageType(enum.Enum):
    e = 0
    n = 1
    v = 2
    s = 3



#A TRANSFORMER EN FIXTURE?????? TROP DE PARAMETRES DANS PARAMETRIZE NON LISBLE APRES
# @pytest.fixture()
# def expected_signal():
#     df = pd.read_csv
#     df.colu
#     return df



@pytest.mark.parametrize("leverage_type, signals_path, returns_path, r_path, positioning_path",
                         [(LeverageType.v.name, "signals_v_to_test", "returns_v_to_test", "r_v_to_test",
                           "positioning_v_to_test"),
                          (LeverageType.s.name, "signals_s_to_test", "returns_s_to_test", "r_s_to_test",
                           "positioning_s_to_test"),
                          (LeverageType.e.name, "signals_e_to_test", "returns_e_to_test", "r_e_to_test",
                           "positioning_e_to_test"),
                          (LeverageType.n.name, "signals_n_to_test", "returns_n_to_test", "r_n_to_test",
                           "positioning_n_to_test")]
                         )
def test_format_data_and_calc(leverage_type, signals_path, returns_path, r_path, positioning_path):
    """
    Function which tests the format_data_and_calc function in order to know if it returns th correct results
    (e.g signals, r, returns, positioning)
    :param data_object: 
    :param signals_path: 
    :param returns_path: 
    :param r_path: 
    :param positioning_path: 
    :return: assertion error if the two compared dataframes are not equal
    """
    data_object = DataTest(leverage=leverage_type, times_inputs=pd.DataFrame, asset_inputs=pd.DataFrame,
                       all_data=pd.DataFrame, signals=pd.DataFrame, returns=pd.DataFrame, r=pd.DataFrame,
                       positioning=pd.DataFrame)
    data_object.set_leverage_from_excel()
    data_object.get_data()
    signals_origin, returns_origin, r_origin, positioning_origin = data_object.get_times_data()

    expected_signals = os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", signals_path))
    expected_returns = os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", returns_path))
    expected_r = os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", r_path))
    expected_positioning = os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", positioning_path))
  
    #expected_output = anais_function()
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



