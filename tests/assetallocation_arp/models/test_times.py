"""
Created on 12/11/2019
Author: AJ89720
email: Anais.Jeremie@lgim.com
"""

import pytest
import os
import pandas as pd
import openpyxl as op
import enum
from assetallocation_arp.models import times
from assetallocation_arp.data_etl import import_data as gd

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
    equal = 0
    normative = 1
    volatility = 2
    standalone = 3

class Data:
    """
    Class Data: set all the necessary data for the times model
    """
    def __init__(self, leverage, times_inputs, asset_inputs, all_data, signals, returns, r, positioning):
        """
        :param leverage: type of the leverage (Equal, Normatiive, Volatility, Standalone)
        :param times_inputs:
        :param asset_inputs:
        :param all_data:
        :param signals:
        :param returns:
        :param r:
        :param positioning:
        """
        self.leverage = leverage
        self.times_inputs = times_inputs
        self.asset_inputs = asset_inputs
        self.all_data = all_data
        self.signals = signals
        self.returns = returns
        self.r = r
        self.positioning = positioning

    def set_leverage_from_excel(self):
        """
        The function allows to change automotatically in the arp_dashboard_test_copy.xlsm the type of the leverage
        :note: the function only works on the copy of the arp_dashboard.xlsm
        """
        #set the workbook arp_dashboard_test_copy
        wb_dashboard = op.load_workbook(os.path.abspath(os.path.join(CURRENT_PATH, "arp_dashboard _test_copy.xlsm")))
        #set the sheet of the current workbook with times_input
        sheet_times = wb_dashboard.get_sheet_by_name('times_input')
        #replace the leverage by the current leverage of the Data Class
        sheet_times['C9'].value = self.leverage
        #save the new workbook with the new leverage (overwrite the current arp_dashboard_copy)
        wb_dashboard.save(os.path.abspath(os.path.join(CURRENT_PATH, "arp_dashboard _test_copy.xlsx")))
        #load the newly created workbook
        xlsm_file = op.load_workbook(os.path.abspath(os.path.join(CURRENT_PATH, "arp_dashboard _test_copy.xlsx")),
                                                     keep_vba=True)
        #save your xlsm file
        xlsm_file.save(os.path.abspath(os.path.join(CURRENT_PATH, "arp_dashboard _test_copy.xlsm")))

    def get_data(self):
        """
        The function gets the different required data for the times model by using the extract_inputs_and_mat_data
        """
        self.times_inputs, self.asset_inputs, self.all_data = gd.extract_inputs_and_mat_data(model_type=Models.times.name,
                                                                                             mat_file=None,
                                                                                             input_file=INPUT_FILE,
                                                                                             model_date=None)
    def get_times_data(self):
        """
        The function returns the computations of the signals, the returns, the r and the positioning regarding the times model
        :return: signals, returns, r, positioning dataframes
        """
        self.signals, self.returns, self.r, self.positioning = times.format_data_and_calc(times_inputs=self.times_inputs,
                                                                                          asset_inputs=self.asset_inputs,
                                                                                          all_data=self.all_data)
        return self.signals, self.returns, self.r, self.positioning

#A TRANSFORMER EN FIXTURE?????? TROP DE PARAMETRES DANS PARAMETRIZE NON LISBLE APRES
# @pytest.fixture()
# def expected_signal():
#     df = pd.read_csv
#     df.colu
#     return df

@pytest.mark.parametrize("data_object, signals_path, returns_path, r_path, positioning_path",
                         [(Data(leverage="v", times_inputs=pd.DataFrame, asset_inputs=pd.DataFrame,
                                all_data=pd.DataFrame,
                                signals=pd.DataFrame, returns=pd.DataFrame, r=pd.DataFrame, positioning=pd.DataFrame),
                                "signals_v_to_test", "returns_v_to_test", "r_v_to_test", "positioning_v_to_test"),

                          (Data(leverage="s", times_inputs=pd.DataFrame, asset_inputs=pd.DataFrame,
                                all_data=pd.DataFrame,
                                signals=pd.DataFrame, returns=pd.DataFrame, r=pd.DataFrame, positioning=pd.DataFrame),
                                "signals_s_to_test", "returns_s_to_test", "r_s_to_test", "positioning_s_to_test"),

                          (Data(leverage="e", times_inputs=pd.DataFrame, asset_inputs=pd.DataFrame,
                                all_data=pd.DataFrame,
                                signals=pd.DataFrame, returns=pd.DataFrame, r=pd.DataFrame, positioning=pd.DataFrame),
                                "signals_e_to_test", "returns_e_to_test", "r_e_to_test", "positioning_e_to_test"),

                          (Data(leverage="n", times_inputs=pd.DataFrame, asset_inputs=pd.DataFrame,
                                all_data=pd.DataFrame,
                                signals=pd.DataFrame, returns=pd.DataFrame, r=pd.DataFrame, positioning=pd.DataFrame),
                                "signals_n_to_test", "returns_n_to_test", "r_n_to_test", "positioning_n_to_test")
                         ])
def test_format_data_and_calc(data_object, signals_path, returns_path, r_path, positioning_path):
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



