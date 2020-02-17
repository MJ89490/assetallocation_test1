import pandas as pd
import numpy as np
import math
import os
import sys
from pandas.tseries.offsets import BDay
from assetallocation_arp.enum import leverage_types
import ARP as arp

TIMES_LAG = 2
CURRENT_PATH = os.path.dirname(__file__)


class ReadData:

    def __init__(self):
        self.settings = pd.DataFrame()
        self.index = pd.DataFrame()
        self.future = pd.DataFrame()
        self.market_select = pd.DataFrame()
        self.costs = pd.DataFrame()
        self._leverage_type = ""
        self.markets = "s_leverage"

    @property
    def leverageType(self):
        return self._leverage_type

    @leverageType.setter
    def leverageType(self, leverage_type):
        self._leverage_type = leverage_type

    def read_data_from_excel(self, path_to_settings, path_to_future, path_to_index):
        self.settings = pd.read_excel(path_to_settings)
        self.settings = self.settings.set_index('Name')
        self.future = pd.read_csv(path_to_future)
        date_timestamp_future = pd.to_datetime(self.future['Date'])
        self.future = self.future.set_index(date_timestamp_future)
        self.index = pd.read_csv(path_to_index)
        date_timestamp_index = pd.to_datetime(self.index['Date'])
        self.index = self.index.set_index(date_timestamp_index)
        del self.index['Date']
        del self.future['Date']
        self.costs = self.settings.loc["costs"]
        self.market_select = self.settings.loc[self.markets]

        return self.future, self.settings, self.index, self.market_select, self.costs


class ComputationsSignals(ReadData):

    def __init__(self):
        ReadData.__init__(self)

    @staticmethod
    def signal_computations():
        sig = pd.DataFrame()
        for column in computations_signals_object.index:
            sig1 = computations_signals_object.index[column].ewm(alpha=2/15).mean()/computations_signals_object.index[column].ewm(alpha=2/30).mean()-1
            sig2 = computations_signals_object.index[column].ewm(alpha=2/30).mean()/computations_signals_object.index[column].ewm(alpha=2/60).mean()-1
            sig3 = computations_signals_object.index[column].ewm(alpha=2/60).mean()/computations_signals_object.index[column].ewm(alpha=2/120).mean()-1
            sig[column] = (sig1/sig1.rolling(window=90).std()+sig2/sig2.rolling(window=90).std()+sig3/sig3.rolling(window=90).std())/3
            sig[column] = sig[column]*np.exp(-1*sig[column].pow(2)/6)/(math.sqrt(3)*math.exp(-0.5))
        sig = arp.discretise(sig, "weekly")
        sig = sig.shift(TIMES_LAG, freq="D")

        return sig

    def leverage_computations(self, future, market_select):
        if computations_signals_object.leverage == leverage_types.Leverage.e.name or computations_signals_object.leverage == leverage_types.Leverage.s.name:
            leverage = 0*future+1
            leverage[computations_signals_object.market_select.index[market_select > 0]] = 1
        elif computations_signals_object.leverage == leverage_types.Leverage.n.name:
            leverage = 0*future + market_select
        elif computations_signals_object.leverage == leverage_types.Leverage.v.name:
            leverage = 1/computations_signals_object.future.ewm(alpha=1/150, min_periods=10).std()
        else:
            raise Exception('Invalid entry')
        leverage[computations_signals_object.market_select.index[computations_signals_object.market_select.isnull()]] = np.nan
        leverage = leverage.shift(periods=TIMES_LAG, freq='D', axis=0).reindex(computations_signals_object.future.append(pd.DataFrame(index=computations_signals_object.future.iloc[[-1]].index+BDay(2))).index, method='pad')

        return leverage

    def positioning_returns_r_computations(self, future, costs, leverage_data):

        if computations_signals_object.leverageType == leverage_types.Leverage.s:
            (ret, R, positioning) = arp.returnTS(ComputationsSignals.signal_computations(), future,
                                                 leverage_data, 0*costs, 0)
            ret1 = ret
            R1 = R
            positioning1 = positioning
        else:
            (ret, R, positioning) = arp.returnTS(ComputationsSignals.signal_computations(), future,
                                                 leverage_data, 0*costs, 1)
            (ret1, R1, positioning1) = arp.rescale(ret, R, positioning, "Total", 0.01)

        return ret1, R1, positioning1


class WriteDataToCsv(ComputationsSignals):

    def __init__(self):
        ComputationsSignals.__init__(self)

    def import_data_to_csv(self, leverage_name, ret1_data, R1_data, positioning_data, signals_data):

        ret1_path = os.path.abspath(os.path.join(CURRENT_PATH, "..", "resources", "ret1_old_"))
        ret1_data.to_csv(f'{ret1_path + leverage_name}', sep='\t', encoding='utf-8')

        R1_path = os.path.abspath(os.path.join(CURRENT_PATH, "..", "resources", "R1_old_"))
        R1_data.to_csv(f'{R1_path + leverage_name}', sep='\t', encoding='utf-8')

        positioning_path = os.path.abspath(os.path.join(CURRENT_PATH, "..", "resources", "positioning_old_"))
        positioning_data.to_csv(f'{positioning_path + leverage_name}', sep='\t', encoding='utf-8')

        signals_path = os.path.abspath(os.path.join(CURRENT_PATH, "..", "resources", "signals_old_"))
        signals_data.to_csv(f'{signals_path + leverage_name}', sep='\t', encoding='utf-8')


if __name__ == "__main__":

    leverage_list = [model.name for model in leverage_types.Leverage]

    for model in leverage_list:

        path_settings = os.path.abspath(os.path.join(CURRENT_PATH, "..", "resources", "settings.xls"))
        path_future = os.path.abspath(os.path.join(CURRENT_PATH, "..", "resources", "futures_data.csv"))
        path_index = os.path.abspath(os.path.join(CURRENT_PATH, "..", "resources", "data.csv"))

        computations_signals_object = ComputationsSignals()

        computations_signals_object.leverage = model

        data_future, data_settings, data_index, data_market_select, data_costs = \
            computations_signals_object.read_data_from_excel(path_to_settings=path_settings,
                                                             path_to_future=path_future,
                                                             path_to_index=path_index)

        signals_data = computations_signals_object.signal_computations()

        leverage = computations_signals_object.leverage_computations(future=data_future, market_select=data_market_select)

        ret1_data, R1_data, positioning_data = \
            computations_signals_object.positioning_returns_r_computations(future=data_future,
                                                                           costs=data_costs,
                                                                           leverage_data=leverage)

        user = input("Would you like to write the results in csv for leverage %s (O or N) ?  " % model)

        if user.lower() == "o":
            write_data_to_csv = WriteDataToCsv()

            write_data_to_csv.import_data_to_csv(leverage_name=computations_signals_object.leverage,
                                                 ret1_data=ret1_data,
                                                 R1_data=R1_data,
                                                 positioning_data=positioning_data,
                                                 signals_data=signals_data)
        else:
            sys.exit(0)
