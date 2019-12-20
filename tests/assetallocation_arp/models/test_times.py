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
import xlwings as xw
CURRENT_PATH = os.path.dirname(__file__)

class Data:
    def __init__(self, leverage, times_inputs, asset_inputs, all_data, signals, returns, r, positioning):
        self.leverage = leverage
        self.times_inputs = times_inputs
        self.asset_inputs = asset_inputs
        self.all_data = all_data
        self.signals = signals
        self.returns = returns
        self.r = r
        self.positioning = positioning

    def set_leverage_from_excel(self):
        wb_dashboard = openpyxl.load_workbook(
            r"C:\Users\AJ89720\PycharmProjects\assetallocation_arp\assetallocation_arp\tests\assetallocation_arp\models\arp_dashboard _test_copy.xlsm")
        print(wb_dashboard.get_sheet_names())

        sheet = wb_dashboard.get_sheet_by_name('times_input')
        print(sheet.title)

        print(sheet['C9'].value)

        sheet['C9'].value = "helloooo"

        print(sheet['C9'].value)

        # save the workbook
        wb_dashboard.save(
            r"C:\Users\AJ89720\PycharmProjects\assetallocation_arp\assetallocation_arp\tests\assetallocation_arp\models\arp_dashboard _test_copy.xlsx")

        # load the newly created workbook
        xlsmFile = openpyxl.load_workbook(
            r"C:\Users\AJ89720\PycharmProjects\assetallocation_arp\assetallocation_arp\tests\assetallocation_arp\models\arp_dashboard _test_copy.xlsx",
            keep_vba=True)

        # save your xlsm file
        xlsmFile.save(
            r"C:\Users\AJ89720\PycharmProjects\assetallocation_arp\assetallocation_arp\tests\assetallocation_arp\models\arp_dashboard _test_copy.xlsm")






        # sht_dashboard.Range("rng_times_inputs").value = self.leverage
        # t = wb_dashboard.range("rng_times_inputs").value

        # df = wb_dashboard.range("C9").value
        # t = "boubou"

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

@pytest.mark.parametrize("data_object, signals_path, returns_path, r_path, positioning_path",
                         [(Data(leverage="v", times_inputs=pd.DataFrame, asset_inputs=pd.DataFrame, all_data=pd.DataFrame, signals=pd.DataFrame, returns=pd.DataFrame, r=pd.DataFrame, positioning=pd.DataFrame),
                           os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", "signals_v_to_test")),os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", "returns_v_to_test")),
                           os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", "r_v_to_test")),os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", "positioning_v_to_test")))
                         ])
def test_format_data_and_calc(data_object, signals_path, returns_path, r_path, positioning_path):

        data_object.set_leverage_from_excel()
        data_object.get_data()
        signals_origin, returns_origin, r_origin, positioning_origin = data_object.get_times_data()







        expected_signals = signals_path
        expected_returns = returns_path
        expected_r = r_path
        expected_positioning = positioning_path
  
        #expected_output = anais_function()
        dataframe_signals = pd.read_csv(expected_signals, index_col=0, sep='\t')
        dataframe_returns = pd.read_csv(expected_returns, index_col=0, sep='\t')
        dataframe_r = pd.read_csv(expected_r, index_col=0, sep='\t')
        dataframe_positioning = pd.read_csv(expected_positioning, index_col=0, sep='\t')

        pd.testing.assert_frame_equal(signals_origin.reset_index(drop=True), dataframe_signals.reset_index(drop=True), check_column_type=False)
        pd.testing.assert_frame_equal(returns_origin.reset_index(drop=True), dataframe_returns.reset_index(drop=True), check_column_type=False)
        pd.testing.assert_frame_equal(r_origin.reset_index(drop=True), dataframe_r.reset_index(drop=True), check_column_type=False)
        pd.testing.assert_frame_equal(positioning_origin.reset_index(drop=True), dataframe_positioning.reset_index(drop=True), check_column_type=False)



