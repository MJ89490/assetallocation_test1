from data_etl.import_data_times import extract_inputs_and_mat_data as data_matlab_effect
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
from assetallocation_arp.data_etl.inputs_effect.write_inputs_effect_excel import get_inputs_matlab_effect

class ImportDataEffect:

    def __init__(self):
        self.data_currencies = pd.DataFrame()

    def import_data_matlab(self):
        """
        Function importing the data from matlab file
        :return: a dataFrame self.data_currencies with matlab data
        """
        self.data_currencies = data_matlab_effect(model_type=Models.effect.name, mat_file=None,
                                                  input_file=None, date=None)

        matlab_inputs = get_inputs_matlab_effect()

        self.data_currencies = self.data_currencies.loc[matlab_inputs['start_date_effect']:]

        self.data_currencies = set_data_frequency(self.data_currencies, matlab_inputs['frequency_effect'],
                                                  matlab_inputs['signal_day_effect'])

        return self.data_currencies


"""
    Class to process data from matlab file
"""


class ProcessDataEffect:

    def __init__(self):
        self.obj_import_data = ImportDataEffect()

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

        preprocess_data = self.preprocess_data_config_effect()
        currencies_usd, currencies_eur, spxt_index = \
            preprocess_data['currencies_usd_config'], preprocess_data['currencies_eur_config'], preprocess_data['spxt_index_values_config']

        data_currencies = self.obj_import_data.import_data_matlab()

        # start_date = '1999-01-06'
        self.data_currencies_usd = data_currencies[currencies_usd.currencies_usd_tickers].loc[:]
        self.data_currencies_eur = data_currencies[currencies_eur.currencies_eur_tickers].loc[:]

        # SPXT Index
        spxt_index_values = data_currencies[spxt_index]

        self.process_data_config_effect()

        return spxt_index_values

    @staticmethod
    def parse_data_config_effect():
        # Instantiate ConfigParser
        config = ConfigParser()
        # Parse existing file
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'config_effect_model', 'all_currencies_effect.ini'))
        config.read(path)
        # Read values from the all_currencies_effect.ini file
        currencies_spot_config = json.loads(config.get('currencies_spot', 'currencies_spot_data'))

        currencies_carry_config = json.loads(config.get('currencies_carry', 'currencies_carry_data'))

        currencies_base_implied_config = json.loads(config.get('currencies_base_implied', 'currencies_base_implied_data'))

        currencies_3M_implied_config = json.loads(config.get('currencies_three_month_implied', '3M_implied_data'))

        spxt_index_config = config.get('spxt_index', 'spxt_index_ticker')

        config_data = {'spot_config': currencies_spot_config,
                       'carry_config': currencies_carry_config,
                       'base_implied_config': currencies_base_implied_config,
                       '3M_implied_config': currencies_3M_implied_config,
                       'spxt_index_config': spxt_index_config}

        return config_data

    def preprocess_data_config_effect(self):
        config_data = self.parse_data_config_effect()

        currencies_3M_implied_usd = config_data['3M_implied_config']['three_month_implied_usd']
        currencies_3M_implied_eur = config_data['3M_implied_config']['three_month_implied_eur']

        currencies_spot_usd = config_data['spot_config']['currencies_spot_usd']
        currencies_spot_eur = config_data['spot_config']['currencies_spot_eur']

        currencies_carry_usd = config_data['carry_config']['currencies_carry_usd']
        currencies_carry_eur = config_data['carry_config']['currencies_carry_eur']

        currencies_base_implied_usd = config_data['base_implied_config']['currencies_base_implied_usd']
        currencies_base_implied_eur = config_data['base_implied_config']['currencies_base_implied_eur']

        spxt_index = config_data['spxt_index_config']

        currencies_usd = pd.DataFrame({"currencies_usd_tickers": currencies_spot_usd + currencies_carry_usd +
                                        currencies_3M_implied_usd + currencies_base_implied_usd})

        currencies_eur = pd.DataFrame({"currencies_eur_tickers": currencies_spot_eur + currencies_carry_eur +
                                        currencies_3M_implied_eur + currencies_base_implied_eur})

        preprocess_data = {'3M_implied_usd_config': currencies_3M_implied_usd,
                           '3M_implied_eur_config': currencies_3M_implied_eur,
                           'spot_usd_config': currencies_spot_usd,
                           'spot_eur_config': currencies_spot_eur,
                           'carry_usd_config': currencies_carry_usd,
                           'carry_eur_config': currencies_carry_eur,
                           'base_implied_usd': currencies_base_implied_usd,
                           'base_implied_eur': currencies_base_implied_eur,
                           'currencies_usd_config': currencies_usd,
                           'currencies_eur_config': currencies_eur,
                           'spxt_index_values_config': spxt_index}

        return preprocess_data

    def process_data_config_effect(self):

        preprocess_data = self.preprocess_data_config_effect()

        self.three_month_implied_usd = self.data_currencies_usd[preprocess_data['3M_implied_usd_config']]
        self.three_month_implied_eur = self.data_currencies_eur[preprocess_data['3M_implied_eur_config']]

        self.spot_usd = self.data_currencies_usd[preprocess_data['spot_usd_config']]
        self.spot_eur = self.data_currencies_eur[preprocess_data['spot_eur_config']]

        self.carry_usd = self.data_currencies_usd[preprocess_data['carry_usd_config']]
        self.carry_eur = self.data_currencies_eur[preprocess_data['carry_eur_config']]

        self.base_implied_usd = self.data_currencies_usd[preprocess_data['base_implied_usd']]
        self.base_implied_eur = self.data_currencies_eur[preprocess_data['base_implied_eur']]

        common_spot = pd.concat([self.spot_usd, self.spot_eur], axis=1)
        common_carry = pd.concat([self.carry_usd, self.carry_eur], axis=1)

        return common_spot, common_carry
