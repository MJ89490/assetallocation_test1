from data_etl.import_data_from_excel_matlab import extract_inputs_and_mat_data as data_matlab_effect
from common_libraries.models_names import Models

from configparser import ConfigParser

import pandas as pd
import os
import sys
import json

import xlwings as xw
import win32api

"""
    Class to import data from matlab file
"""

from assetallocation_arp.data_etl.data_manipulation import set_data_frequency


class ImportDataEffect:

    def __init__(self, end_date_mat, start_date_mat, frequency_mat, signal_day_mat, all_data):
        self.data_currencies = pd.DataFrame()
        self.frequency_mat = frequency_mat
        self.start_date_mat = start_date_mat
        self.signal_day_mat = signal_day_mat
        self.end_date_mat = end_date_mat
        self.all_data = all_data

    @property
    def frequency_mat(self):
        return self._frequency_mat

    @frequency_mat.setter
    def frequency_mat(self, value):
        self._frequency_mat = value

    @property
    def start_date_mat(self):
        return self._start_date_mat

    @start_date_mat.setter
    def start_date_mat(self, value):
        self._start_date_mat = value

    @property
    def end_date_mat(self):
        return self._end_date_mat

    @end_date_mat.setter
    def end_date_mat(self, value):
        self._end_date_mat = value

    @property
    def signal_day_mat(self):
        return self._signal_day_mat

    @signal_day_mat.setter
    def signal_day_mat(self, value):
        self._signal_day_mat = value

    def import_data_matlab(self):
        """
        Function importing the data from matlab file
        :return: a dataFrame self.data_currencies with matlab data
        """
        # self.data_currencies = data_matlab_effect(model_type=Models.effect.name, mat_file=None,
        #                                           input_file=None, model_date=None)
        self.data_currencies = self.all_data
        self.data_currencies = self.data_currencies.loc[self.start_date_mat:self.end_date_mat]

        self.data_currencies = set_data_frequency(self.data_currencies, self.frequency_mat, self.signal_day_mat)

        return self.data_currencies


"""
    Class to process data from matlab file
"""


class ProcessDataEffect:

    def __init__(self, asset_inputs, frequency_mat, start_date_mat, end_date_mat, signal_day_mat, all_data):
        self.obj_import_data = ImportDataEffect(frequency_mat=frequency_mat, start_date_mat=start_date_mat, end_date_mat=end_date_mat, signal_day_mat=signal_day_mat, all_data=all_data)

        self.data_currencies = pd.DataFrame()
        self.data_currencies_usd = pd.DataFrame()
        self.data_currencies_eur = pd.DataFrame()

        self.three_month_implied_usd = pd.DataFrame()
        self.three_month_implied_eur = pd.DataFrame()
        self.spot_usd = pd.DataFrame()
        self.spot_eur = pd.DataFrame()
        self.carry_usd = pd.DataFrame()
        self.carry_eur = pd.DataFrame()
        self.base_implied_usd = pd.DataFrame()
        self.base_implied_eur = pd.DataFrame()

        self.start_date_calculations = ''

        self.asset_inputs = asset_inputs
        self.currencies_spot, self.currencies_carry = dict(), dict()
        self.currencies_3M_implied, self.currencies_base_implied_usd = dict(), dict()

    @property
    def currencies_spot(self):
        return self._currencies_spot

    @currencies_spot.setter
    def currencies_spot(self, value):
        self._currencies_spot = value

    @property
    def all_currencies_spot(self):
        spot = list(map(self._currencies_spot.get, self._currencies_spot.keys()))
        return [item for elem in spot for item in elem]

    @property
    def all_currencies_carry(self):
        carry = list(map(self._currencies_carry.get, self._currencies_carry.keys()))
        return [item for elem in carry for item in elem]

    @property
    def all_currencies_3M_implied(self):
        implied = list(map(self._currencies_3M_implied.get, self._currencies_3M_implied.keys()))
        return [item for elem in implied for item in elem]

    @property
    def currencies_carry(self):
        return self._currencies_carry

    @currencies_carry.setter
    def currencies_carry(self, value):
        self._currencies_carry = value

    @property
    def currencies_3M_implied(self):
        return self._currencies_3M_implied

    @currencies_3M_implied.setter
    def currencies_3M_implied(self, value):
        self._currencies_3M_implied = value

    @property
    def dates_index(self):
        start_current_date_index_loc = self.data_currencies_usd.index.get_loc(self.start_date_calculations)
        new_start_date_index = self.data_currencies_usd.index[start_current_date_index_loc - 1]

        return pd.to_datetime(self.data_currencies_usd.loc[new_start_date_index:].index.values, format='%d-%m-%Y')

    @property
    def dates_origin_index(self):
        return pd.to_datetime(self.data_currencies_usd.loc[self.start_date_calculations:].index.values, format='%d-%m-%Y')

    @property
    def start_date_calculations(self):
        return self._start_date_calculations

    @start_date_calculations.setter
    def start_date_calculations(self, value):
        # Instantiate ConfigParser
        config = ConfigParser()
        # Parse existing file
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'config_effect_model', 'dates_effect.ini'))
        config.read(path)
        # Read values from the dates_effect.ini file
        start_common_date = config.get('common_start_date_effect', 'start_common_data')

        if value == '':
            self._start_date_calculations = None
        else:
            if pd.to_datetime(value, format='%d-%m-%Y') < pd.to_datetime(start_common_date, format='%d-%m-%Y'):
                wb = xw.Book.caller()
                win32api.MessageBox(wb.app.hwnd, f'Start date is lesser than {start_common_date}')
                sys.exit()
                # raise ValueError(f'Start date is lesser than {start_common_date}')
            else:
                start_date = self.find_date(self.data_currencies_usd.index.values, pd.to_datetime(value, format='%d-%m-%Y'))
                self._start_date_calculations = start_date

    @staticmethod
    def find_date(dates_set, pivot):
        flag = False
        # Initialization to start the while loop
        counter = 0
        date = dates_set[0]

        while pivot > date:
            counter += 1
            if counter >= len(dates_set):
                # Reach the end of the dates_set list
                flag = True
                break
            date = dates_set[counter]
        else:
            if pivot == date:
                t_start = pivot
            else:
                t_start = dates_set[counter - 1]

        # End of the list, we set the date to the last date
        if flag:
            t_start = dates_set[-1]

        return t_start

    def process_data_effect(self):
        """
        Function processing data from the matlab file to get the required data
        :return: two dataFrames self.data_currencies_usd, self.data_currencies_eur for usd and eur currencies
        """

        parse_data = self.parse_data_excel_effect()

        currencies_usd = pd.DataFrame({"currencies_usd_tickers": parse_data['spot_config']['currencies_spot_usd'] +
                                                                 parse_data['carry_config']['currencies_carry_usd'] +
                                                                 parse_data['3M_implied_config']['three_month_implied_usd'] +
                                                                 parse_data['base_implied_config']['currencies_base_implied_usd']})

        currencies_eur = pd.DataFrame({"currencies_eur_tickers": parse_data['spot_config']['currencies_spot_eur'] +
                                                                 parse_data['carry_config']['currencies_carry_eur'] +
                                                                 parse_data['3M_implied_config']['three_month_implied_eur'] +
                                                                 parse_data['base_implied_config']['currencies_base_implied_eur']})

        self.data_currencies = self.obj_import_data.import_data_matlab()

        # start_date = '1999-01-06'
        self.data_currencies_usd = self.data_currencies[currencies_usd.currencies_usd_tickers].loc[:]
        self.data_currencies_eur = self.data_currencies[currencies_eur.currencies_eur_tickers].loc[:]

        # SPXT Index
        spxt_index_values = self.data_currencies[parse_data['spxt_index_config']]

        self.process_data_config_effect()

        return spxt_index_values

    def parse_data_excel_effect(self):

        """
        Function parsing the data from the config file
        :return: a dictionary
        """
        # Instantiate ConfigParser
        config = ConfigParser()
        # Parse existing file
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'config_effect_model', 'all_currencies_effect.ini'))
        config.read(path)
        # Read values from the all_currencies_effect_to_delete.ini file
        currencies_base_implied_config = json.loads(config.get('currencies_base_implied', 'currencies_base_implied_data'))
        # Read value from Excel and sort data depending on its base currency
        currencies_eur = self.asset_inputs.loc[self.asset_inputs['EUR/USD base'] == 'EUR']
        currencies_usd = self.asset_inputs.loc[self.asset_inputs['EUR/USD base'] == 'USD']

        self.currencies_spot['currencies_spot_usd'] = currencies_usd['Spot ticker'].tolist()
        self.currencies_spot['currencies_spot_eur'] = currencies_eur['Spot ticker'].tolist()

        self.currencies_carry['currencies_carry_usd'] = currencies_usd['Carry ticker'].tolist()
        self.currencies_carry['currencies_carry_eur'] = currencies_eur['Carry ticker'].tolist()

        self.currencies_3M_implied['three_month_implied_usd'] = currencies_usd['3M implied ticker'].tolist()
        self.currencies_3M_implied['three_month_implied_eur'] = currencies_eur['3M implied ticker'].tolist()

        inflation_config_bbg = pd.concat([self.asset_inputs['Inflation currency ticker'], self.asset_inputs['inflation base currency ticker'].iloc[:3]], axis=0)

        # SPX Index
        spxt_index_config = config.get('spxt_index', 'spxt_index_ticker')

        config_data = {'spot_config': self.currencies_spot,
                       'carry_config': self.currencies_carry,
                       'base_implied_config': currencies_base_implied_config,
                       '3M_implied_config': self.currencies_3M_implied,
                       'spxt_index_config': spxt_index_config,
                       'inflation_config_bbg': inflation_config_bbg}

        return config_data

    def process_data_config_effect(self):
        """
        Function processing the data from the config file
        :return: dataFrames for spot and carry
        """

        assets_table = self.parse_data_excel_effect()

        self.three_month_implied_usd = self.data_currencies_usd[assets_table['3M_implied_config']['three_month_implied_usd']]
        self.three_month_implied_eur = self.data_currencies_eur[assets_table['3M_implied_config']['three_month_implied_eur']]

        self.spot_usd = self.data_currencies_usd[assets_table['spot_config']['currencies_spot_usd']]
        self.spot_eur = self.data_currencies_eur[assets_table['spot_config']['currencies_spot_eur']]

        self.carry_usd = self.data_currencies_usd[assets_table['carry_config']['currencies_carry_usd']]
        self.carry_eur = self.data_currencies_eur[assets_table['carry_config']['currencies_carry_eur']]

        self.base_implied_usd = self.data_currencies_usd[assets_table['base_implied_config']['currencies_base_implied_usd']]
        self.base_implied_eur = self.data_currencies_eur[assets_table['base_implied_config']['currencies_base_implied_eur']]

        common_spot = pd.concat([self.spot_usd, self.spot_eur], axis=1)
        common_carry = pd.concat([self.carry_usd, self.carry_eur], axis=1)

        inflaton_bbg = self.data_currencies[assets_table['inflation_config_bbg']]

        rng = pd.date_range(start=inflaton_bbg.index[0], end=inflaton_bbg.index[-1], freq='Y')
        sig = inflaton_bbg.reindex(rng, method='pad')


        inflaton_bbg.columns = pd.concat([self.asset_inputs['Spot ticker'], pd.Series(['EUR', 'GBP', 'USD'])], axis=0)
        inflaton_bbg = inflaton_bbg.set_index(inflaton_bbg.index.year)
        return common_spot, common_carry, inflaton_bbg
