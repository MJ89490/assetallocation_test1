import os
import sys
import json
import win32api

import xlwings as xw
import pandas as pd

from configparser import ConfigParser

from assetallocation_arp.data_etl.inputs_effect.import_data_effect import ImportDataEffect

"""
    Class to process data from matlab file
"""

#TODO SIMPLIFY THE CLASS

class ProcessDataEffect:

    def __init__(self, asset_inputs, frequency_mat, end_date_mat, signal_day_mat, all_data):
        self.obj_import_data = ImportDataEffect(frequency_mat=frequency_mat, end_date_mat=end_date_mat,
                                                signal_day_mat=signal_day_mat, all_data=all_data)

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
        self.eur_usd_cr = pd.DataFrame()

        self.start_date_calculations = ''

        self.asset_inputs = asset_inputs
        self.currencies_spot, self.currencies_carry = dict(), dict()
        self.currencies_3M_implied, self.currencies_base_implied_usd = dict(), dict()
        self.weight_percentage_usd = pd.DataFrame()
        self.weight_percentage_eur = pd.DataFrame()


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
        start_current_date_index_loc = self.obj_import_data.data_currencies_copy.index.get_loc(self.start_date_calculations)
        new_start_date_index = self.obj_import_data.data_currencies_copy.index[start_current_date_index_loc - 1]

        return pd.to_datetime(self.obj_import_data.data_currencies_copy.loc[new_start_date_index:].index.values, format='%d-%m-%Y')

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

    @property
    def previous_start_date_calc(self):
        start_current_date_index_loc = self.obj_import_data.data_currencies_copy.index.get_loc(self.start_date_calculations)
        return self.obj_import_data.data_currencies_copy.index[start_current_date_index_loc - 1]

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
                                       parse_data['carry_config']['currencies_carry_usd']})

        currencies_eur = pd.DataFrame({"currencies_eur_tickers": parse_data['spot_config']['currencies_spot_eur'] +
                                       parse_data['carry_config']['currencies_carry_eur']})

        implied_usd = pd.DataFrame({"currencies_usd_tickers": parse_data['3M_implied_config']['three_month_implied_usd']
                                    + parse_data['base_implied_config']['currencies_base_implied_usd']})

        implied_eur = pd.DataFrame({"currencies_eur_tickers": parse_data['3M_implied_config']['three_month_implied_eur']
                                    + parse_data['base_implied_config']['currencies_base_implied_eur']})

        self.data_currencies = self.obj_import_data.import_data_matlab('na')
        data_currencies_average = self.obj_import_data.import_data_matlab('average')

        self.data_currencies_usd = pd.concat([self.data_currencies[currencies_usd.currencies_usd_tickers].loc[:],
                                              data_currencies_average[implied_usd.currencies_usd_tickers].loc[:]],
                                             axis=1)
        self.data_currencies_eur = pd.concat([self.data_currencies[currencies_eur.currencies_eur_tickers].loc[:],
                                              data_currencies_average[implied_eur.currencies_eur_tickers].loc[:]],
                                             axis=1)
        # SPXT Index
        spxt_index_values = self.data_currencies[parse_data['spxt_index_config']]

        self.process_data_config_effect()

        return spxt_index_values

    def parse_data_excel_effect(self):
        """
        Function parsing the data from the config file and from excel
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

        weight_usd = list(currencies_usd['Weight on USD'].apply(lambda x: x * 100))
        weight_eur = list(currencies_eur['Weight on USD'].apply(lambda x: x * 100))

        self.weight_percentage_usd = pd.DataFrame(weight_usd, index=list(currencies_usd['Spot ticker'])).transpose()
        self.weight_percentage_eur = pd.DataFrame(weight_eur, index=list(currencies_eur['Spot ticker'])).transpose()

        # SPX Index
        spxt_index_config = config.get('spxt_index', 'spxt_index_ticker')

        # EURUSDCR Curncy
        eur_usd_cr_config = config.get('EURUSDCR Currency', 'eur_usd_cr_ticker')

        config_data = {'spot_config': self.currencies_spot,
                       'carry_config': self.currencies_carry,
                       'base_implied_config': currencies_base_implied_config,
                       '3M_implied_config': self.currencies_3M_implied,
                       'spxt_index_config': spxt_index_config,
                       'eur_usd_cr_config': eur_usd_cr_config}

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

        self.eur_usd_cr = self.data_currencies[assets_table['eur_usd_cr_config']]

        common_spot = pd.concat([self.spot_usd, self.spot_eur], axis=1)
        common_carry = pd.concat([self.carry_usd, self.carry_eur], axis=1)

        return common_spot, common_carry
