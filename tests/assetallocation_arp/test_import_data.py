from assetallocation_arp.models import times
from assetallocation_arp.data_etl import import_data as gd
import pandas as pd


class Data:
    def __init__(self):
        self.leverage = "v"
        self.times_inputs = pd.DataFrame()
        self.asset_inputs = pd.DataFrame()
        self.all_data = pd.DataFrame()
        self.signals = pd.DataFrame()
        self.returns = pd.DataFrame()
        self.r = pd.DataFrame()
        self.positioning = pd.DataFrame()

    def get_data(self):
        self.times_inputs, self.asset_inputs, self.all_data = gd.extract_inputs_and_mat_data("times", None, None)
        return 2+2
    def get_times_data(self):
        self.signals, self.returns, self.r, self.positioning = times.format_data_and_calc(self.times_inputs,
                                                                                          self.asset_inputs,
                                                                                          self.all_data)


if __name__ == "__main__":
    obj = Data()
    x = obj.get_data()