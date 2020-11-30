import os
import json

import pandas as pd
import numpy as np

from configparser import ConfigParser

from assetallocation_arp.data_etl.inputs_effect.import_data_effect import ImportDataEffect
from assetallocation_arp.data_etl.inputs_effect.find_date import find_date

"""
    Class to process data from matlab file
"""


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
    
    @property
    def start_date_prev_calculations(self):
        start_current_date_index_loc = self.obj_import_data.data_currencies_copy.index.get_loc(self.start_date_calculations)
        return self.obj_import_data.data_currencies_copy.index[start_current_date_index_loc - 1]

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
                raise ValueError(f'Start date is lesser than {start_common_date}')
            else:
                start_date = find_date(self.data_currencies_usd.index.values, pd.to_datetime(value, format='%d-%m-%Y'))
                self._start_date_calculations = start_date

    @property
    def previous_start_date_calc(self):
        start_current_date_index_loc = self.obj_import_data.data_currencies_copy.index.get_loc(self.start_date_calculations)
        return self.obj_import_data.data_currencies_copy.index[start_current_date_index_loc - 1]

    def process_all_data_effect(self):
        """
        Function processing data from the matlab file to get the required data
        :return: two dataFrames self.data_currencies_usd, self.data_currencies_eur for usd and eur currencies
        """

        parse_data = self.parse_data_config_effect()

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

        self.process_usd_eur_data_effect()

    def parse_data_config_effect(self):
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
        currencies_eur = self.asset_inputs.loc[self.asset_inputs['input_usd_eur'] == 'EUR']
        currencies_usd = self.asset_inputs.loc[self.asset_inputs['input_usd_eur'] == 'USD']

        # Region values to create a region dict with currency list as values
        region = {}

        unique_region = np.unique(self.asset_inputs['input_region'].to_list())

        for reg in unique_region:
            region_tmp = self.asset_inputs.loc[self.asset_inputs['input_region'] == reg]
            curr = ['Combo_' + val for val in region_tmp['input_spot_ticker'].to_list()]
            region[reg.lower()] = curr

        self.currencies_spot['currencies_spot_usd'] = currencies_usd['input_spot_ticker'].tolist()
        self.currencies_spot['currencies_spot_eur'] = currencies_eur['input_spot_ticker'].tolist()

        self.currencies_carry['currencies_carry_usd'] = currencies_usd['input_carry_ticker'].tolist()
        self.currencies_carry['currencies_carry_eur'] = currencies_eur['input_carry_ticker'].tolist()

        self.currencies_3M_implied['three_month_implied_usd'] = currencies_usd['input_implied'].tolist()
        self.currencies_3M_implied['three_month_implied_eur'] = currencies_eur['input_implied'].tolist()

        weight_usd = list(currencies_usd['input_weight_usd'])
        weight_eur = list(currencies_eur['input_weight_usd'])

        self.weight_percentage_usd = pd.DataFrame(weight_usd, index=list(currencies_usd['input_spot_ticker'])).transpose()
        self.weight_percentage_eur = pd.DataFrame(weight_eur, index=list(currencies_eur['input_spot_ticker'])).transpose()

        # SPX Index
        spxt_index_config = config.get('spxt_index', 'spxt_index_ticker')

        # EURUSDCR Curncy
        eur_usd_cr_config = config.get('eurusdcr_currency', 'eur_usd_cr_ticker')

        # JGENVUUG Index
        jgenvuug_index_config = config.get('jgenvuug_index', 'jgenvuug_index_ticker')

        config_data = {'spot_config': self.currencies_spot,
                       'carry_config': self.currencies_carry,
                       'base_implied_config': currencies_base_implied_config,
                       '3M_implied_config': self.currencies_3M_implied,
                       'spxt_index_config': spxt_index_config,
                       'eur_usd_cr_config': eur_usd_cr_config,
                       'jgenvuug_index_config': jgenvuug_index_config,
                       'region_config': region}

        return config_data

    def process_usd_eur_data_effect(self):
        """
        Function processing the data from the config file
        :return: dataFrames for spot and carry
        """

        assets_table = self.parse_data_config_effect()

        self.three_month_implied_usd = self.data_currencies_usd[assets_table['3M_implied_config']['three_month_implied_usd']]
        self.three_month_implied_eur = self.data_currencies_eur[assets_table['3M_implied_config']['three_month_implied_eur']]

        self.spot_usd = self.data_currencies_usd[assets_table['spot_config']['currencies_spot_usd']]
        self.spot_eur = self.data_currencies_eur[assets_table['spot_config']['currencies_spot_eur']]

        self.carry_usd = self.data_currencies_usd[assets_table['carry_config']['currencies_carry_usd']]
        self.carry_eur = self.data_currencies_eur[assets_table['carry_config']['currencies_carry_eur']]

        self.base_implied_usd = self.data_currencies_usd[assets_table['base_implied_config']['currencies_base_implied_usd']]
        self.base_implied_eur = self.data_currencies_eur[assets_table['base_implied_config']['currencies_base_implied_eur']]

        self.eur_usd_cr = self.data_currencies[assets_table['eur_usd_cr_config']]

        spxt_index_values = self.data_currencies[assets_table['spxt_index_config']]

        jgenvuug_index_values = self.data_currencies[assets_table['jgenvuug_index_config']]

        common_spot = pd.concat([self.spot_usd, self.spot_eur], axis=1)
        common_carry = pd.concat([self.carry_usd, self.carry_eur], axis=1)

        return {'common_spot': common_spot, 'common_carry': common_carry, 'spxt_index_values': spxt_index_values,
                'three_month_implied_usd': self.three_month_implied_usd,
                'three_month_implied_eur': self.three_month_implied_eur,
                'region_config': assets_table['region_config'], 'jgenvuug_index_values': jgenvuug_index_values}
