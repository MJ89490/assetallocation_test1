"""
Created on 17/02/2020
Author: AJ89720
email: Anais.Jeremie@lgim.com
"""

import os

import pandas as pd
import sys

from assetallocation_arp.models import times
from assetallocation_arp.data_etl import import_data as gd
from assetallocation_arp.enum import models_names as models
from assetallocation_arp.enum import leverage_types

CURRENT_PATH = os.path.dirname(__file__)
INPUT_FILE = os.path.abspath(os.path.join(CURRENT_PATH, "..", "regression_test", "resources", "arp_dashboard_test_copy.xlsm"))


class DataTimes:
    """
    Class DataTest: set all the necessary data for the times model testing
    """
    def __init__(self):
        """
        :param leverage: type of the leverage (Equal, Normative, Volatility, Standalone)
        """
        self._leverage_type = ""
        self.times_inputs = pd.DataFrame
        self.asset_inputs = pd.DataFrame
        self.all_data = pd.DataFrame
        self.signals = pd.DataFrame
        self.returns = pd.DataFrame
        self.r = pd.DataFrame
        self.positioning = pd.DataFrame
        self.strategy_inputs = pd.DataFrame

    @property
    def leverageType(self):
        return self._leverage_type

    @leverageType.setter
    def leverageType(self, leverage_type):
        self._leverage_type = leverage_type

    def get_data(self):
        """
        The function gets the different required data for the times model by using the extract_inputs_and_mat_data
        """
        self.strategy_inputs, self.asset_inputs, self.all_data = gd.extract_inputs_and_mat_data(model_type=models.Models.times.name,
                                                                                                mat_file=None,
                                                                                                input_file=INPUT_FILE,
                                                                                                model_date=None)

        leverage_file_name = f'times_inputs_{self._leverage_type}_leverage'
        strategy_inputs_expected = os.path.abspath(os.path.join(CURRENT_PATH, "resources", leverage_file_name))
        self.times_inputs = pd.read_csv(strategy_inputs_expected, index_col=0)

        return self.times_inputs, self.asset_inputs, self.all_data

    def get_times_model_data(self, times_inputs, asset_inputs, all_data):
        """
        The function returns the computations of the signals, the returns, the r and the positioning regarding the times model
        """
        self.signals, self.returns, self.r, self.positioning = times.format_data_and_calc(times_inputs=times_inputs,
                                                                                          asset_inputs=asset_inputs,
                                                                                          all_data=all_data)
        return self.signals, self.returns, self.r, self.positioning


class WriteDataToCsv(DataTimes):

    def __init__(self):
        DataTimes.__init__(self)

    @staticmethod
    def import_data_to_csv(leverage_name, returns, r, positioning, signals):

        returns_path = os.path.abspath(os.path.join(CURRENT_PATH, "..", "regression_test", "resources", "ret1_new_"))
        returns.to_csv(f'{returns_path + leverage_name}', encoding='utf-8', index=False)

        r_path = os.path.abspath(os.path.join(CURRENT_PATH, "..", "regression_test", "resources", "R1_new_"))
        r.to_csv(f'{r_path + leverage_name}', encoding='utf-8', index=False)

        positioning_path = os.path.abspath(os.path.join(CURRENT_PATH, "..", "regression_test", "resources", "positioning_new_"))
        positioning.to_csv(f'{positioning_path + leverage_name}', encoding='utf-8', index=False)

        signals_path = os.path.abspath(os.path.join(CURRENT_PATH, "..", "regression_test", "resources", "signals_new_"))
        signals.to_csv(f'{signals_path + leverage_name}', encoding='utf-8', index=False)


if __name__ == "__main__":

    leverage_list = [model.name for model in leverage_types.Leverage]

    for model in leverage_list:
        data_times_object = DataTimes()
        data_times_object.leverageType = model
        times_inputs_data, asset_inputs_data, all_data_matlab = data_times_object.get_data()
        signals_data, returns_data, r_data, positioning_data = data_times_object.get_times_model_data(
                                                                                        times_inputs=times_inputs_data,
                                                                                        asset_inputs=asset_inputs_data,
                                                                                        all_data=all_data_matlab)

        user = input("Would you like to write the results in csv for leverage %s (O or N) ?  " % model)

        if user.lower() == "o":
            write_data_to_csv_object = WriteDataToCsv()
            write_data_to_csv_object.import_data_to_csv(leverage_name=model,
                                                        returns=returns_data,
                                                        r=r_data,
                                                        positioning=positioning_data,
                                                        signals=signals_data)
        else:
            sys.exit(0)
