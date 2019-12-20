from assetallocation_arp.models import times
from assetallocation_arp.data_etl import import_data as gd
import pandas as pd


# class Data(object):
#     def __init__(self, times_inputs, asset_inputs, all_data, signals, returns, r, positioning):
#         self.leverage = "v"
#         self.times_inputs = times_inputs
#         self.asset_inputs = asset_inputs
#         self.all_data = all_data
#         self.signals = signals
#         self.returns = returns
#         self.r = r
#         self.positioning = positioning
#
#     def get_data(self):
#         self.times_inputs, self.asset_inputs, self.all_data = gd.extract_inputs_and_mat_data("times", None, None)
#         #return self.times_inputs, self.asset_inputs, self.all_data
#
#     def get_times_data(self): #, times_inputs, asset_inputs, all_data, signals, returns, r, positioning):
#         self.signals, self.returns, self.r, self.positioning = times.format_data_and_calc(self.times_inputs, self.asset_inputs, self.all_data)
#         return self.signals, self.returns, self.r, self.positioning

# class Test(Data):
#     def __init__(self, times_input, asset_inputs, all_data, signals, returns, r, positioning):
#         Data.__init__(self, times_input, asset_inputs, all_data, signals, returns, r, positioning)
#
#     def test_format_data_and_calc(self):
#         Test.get_data(self)
#         signals, returns, r, positioning = Test.get_times_data(self)
#
#         return signals, returns, r, positioning
# class UnitTestt(Data):
#     def __init__(self, times_input, asset_inputs, all_data, signals, returns, r, positioning):
#         Data.__init__(self, times_input, asset_inputs, all_data, signals, returns, r, positioning)
#
#     def test_format_data_and_calc(self):
#         UnitTestt.get_data(self)
#         signals, returns, r, positioning = UnitTestt.get_times_data(self)
#
#         expected_signals = os.path.abspath(os.path.join(CURRENT_PATH, "..", "data_times_to_test", "signals_v_to_test"))
#         d_expected = pd.read_csv(expected_signals, index_col=0, sep='\t')
#         pd.testing.assert_frame_equal(returns.reset_index(drop=True), d_expected.reset_index(drop=True),
#                                       check_column_type=False)
#         #return signals, returns, r, positioning

import openpyxl

def set_leverage_from_excel():

    wb_dashboard = openpyxl.load_workbook(r"C:\Users\AJ89720\PycharmProjects\assetallocation_arp\assetallocation_arp\tests\assetallocation_arp\models\arp_dashboard _test_copy.xlsm")
    print(wb_dashboard.get_sheet_names())

    sheet = wb_dashboard.get_sheet_by_name('times_input')
    print(sheet.title)

    print(sheet['C9'].value)

    sheet['C9'].value = "helloooo"

    print(sheet['C9'].value)

    # save the workbook
    wb_dashboard.save(r"C:\Users\AJ89720\PycharmProjects\assetallocation_arp\assetallocation_arp\tests\assetallocation_arp\models\arp_dashboard _test_copy.xlsx")

    # load the newly created workbook
    xlsmFile = openpyxl.load_workbook(r"C:\Users\AJ89720\PycharmProjects\assetallocation_arp\assetallocation_arp\tests\assetallocation_arp\models\arp_dashboard _test_copy.xlsx", keep_vba=True)

    # save your xlsm file
    xlsmFile.save(r"C:\Users\AJ89720\PycharmProjects\assetallocation_arp\assetallocation_arp\tests\assetallocation_arp\models\arp_dashboard _test_copy.xlsm")


if __name__ == "__main__":

    set_leverage_from_excel()
    # times_input = pd.DataFrame
    # asset_inputs = pd.DataFrame
    # all_data = pd.DataFrame
    # signals = pd.DataFrame
    # returns = pd.DataFrame
    # r = pd.DataFrame
    # positioning = pd.DataFrame
    #
    # obj2 = Test(times_input, asset_inputs, all_data, signals, returns, r, positioning)
    # obj2.test_format_data_and_calc()
