import openpyxl as op
import os
import pandas as pd

from assetallocation_arp.models import times
from assetallocation_arp.data_etl import import_data as gd
from assetallocation_arp.enum import ModelsNames as models

CURRENT_PATH = os.path.dirname(__file__)
INPUT_FILE = os.path.abspath(os.path.join(CURRENT_PATH, "arp_dashboard _test_copy.xlsm"))


class DataTest:
    """
    Class DataTest: set all the necessary data for the times model testing
    """
    def __init__(self, leverage):
        """
        :param leverage: type of the leverage (Equal, Normative, Volatility, Standalone)
        :param times_inputs:
        :param asset_inputs:
        :param all_data:
        :param signals:
        :param returns:
        :param r:
        :param positioning:
        """
        self.leverage = leverage
        self.times_inputs = pd.DataFrame
        self.asset_inputs = pd.DataFrame
        self.all_data = pd.DataFrame
        self.signals = pd.DataFrame
        self.returns = pd.DataFrame
        self.r = pd.DataFrame
        self.positioning = pd.DataFrame

    @property
    def getter_times_inputs(self):
        return self.times_inputs
    @property
    def getter_asset_inputs(self):
        return self.asset_inputs
    @property
    def getter_all_data(self):
        return self.all_data
    @property
    def getter_signals(self):
        return self.signals
    @property
    def getter_returns(self):
        return self.returns
    @property
    def getter_r(self):
        return self.r
    @property
    def getter_positioning(self):
        return self.positioning

    def set_leverage_from_excel(self):
        """
        The function allows to change automatically in the arp_dashboard_test_copy.xlsm the type of the leverage
        :noteworthy: the function only works on the copy of the arp_dashboard.xlsm
        """
        # set the workbook arp_dashboard_test_copy
        wb_dashboard = op.load_workbook(os.path.abspath(os.path.join(CURRENT_PATH, "arp_dashboard _test_copy.xlsm")))
        # set the sheet of the current workbook with times_input
        sheet_times = wb_dashboard.get_sheet_by_name('times_input')
        # replace the leverage by the current leverage of the Data Class
        sheet_times['C9'].value = self.leverage
        # save the new workbook with the new leverage (overwrite the current arp_dashboard_copy)
        wb_dashboard.save(os.path.abspath(os.path.join(CURRENT_PATH, "arp_dashboard _test_copy.xlsx")))
        # load the newly created workbook
        xlsm_file = op.load_workbook(os.path.abspath(os.path.join(CURRENT_PATH, "arp_dashboard _test_copy.xlsx")),
                                                     keep_vba=True)
        # save your xlsm file
        xlsm_file.save(os.path.abspath(os.path.join(CURRENT_PATH, "arp_dashboard _test_copy.xlsm")))

    def get_data(self):
        """
        The function gets the different required data for the times model by using the extract_inputs_and_mat_data
        """
        self.times_inputs, self.asset_inputs, self.all_data = gd.extract_inputs_and_mat_data(model_type=models.Models.times.name,
                                                                                             mat_file=None,
                                                                                             input_file=INPUT_FILE,
                                                                                             model_date=None)

    def get_times_model_data(self):
        """
        The function returns the computations of the signals, the returns, the r and the positioning regarding the times model
        """
        self.signals, self.returns, self.r, self.positioning = times.format_data_and_calc(times_inputs=self.times_inputs,
                                                                                          asset_inputs=self.asset_inputs,
                                                                                          all_data=self.all_data)
