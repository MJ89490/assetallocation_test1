import openpyxl as op
import os
import enum

from assetallocation_arp.models import times
from assetallocation_arp.data_etl import import_data as gd

CURRENT_PATH = os.path.dirname(__file__)
INPUT_FILE = os.path.abspath(os.path.join(CURRENT_PATH, "arp_dashboard _test_copy.xlsm"))

class Models(enum.Enum):
    times = 0
    maven = 1
    effect = 2
    curp = 3
    fica = 4
    factor = 5
    comca = 6

class DataTest:
    """
    Class Data: set all the necessary data for the times model testing
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