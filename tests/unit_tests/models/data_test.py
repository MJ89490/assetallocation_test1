import os

import pandas as pd

from assetallocation_arp.models import times
from assetallocation_arp.data_etl import import_data as gd
from assetallocation_arp.enum import models_names as models

CURRENT_PATH = os.path.dirname(__file__)


class DataTest:
    """
    Class DataTest: set all the necessary data for the times model testing
    """
    def __init__(self, leverage):
        """
        :param leverage: type of the leverage (Equal, Normative, Volatility, Standalone)
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

    def get_data(self):
        """
        The function gets the different required data for the times model by using the extract_inputs_and_mat_data
        """
        not_needed_for_test, self.asset_inputs, self.all_data = gd.extract_inputs_and_mat_data(model_type=models.Models.times.name,
                                                                                               mat_file=None,
                                                                                               input_file=None,
                                                                                               model_date=None)

        leverage_file_name = f'times_inputs_{self.leverage}_leverage'
        strategy_inputs_expected = os.path.abspath(os.path.join(CURRENT_PATH, "resources", leverage_file_name))
        self.times_inputs = pd.read_csv(strategy_inputs_expected, index_col=0)

    def get_times_model_data(self):
        """
        The function returns the computations of the signals, the returns, the r and the positioning regarding the times model
        """
        self.signals, self.returns, self.r, self.positioning = times.format_data_and_calc(times_inputs=self.times_inputs,
                                                                                          asset_inputs=self.asset_inputs,
                                                                                          all_data=self.all_data)
