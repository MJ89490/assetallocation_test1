from datetime import timedelta, datetime
from pandas.tseries import offsets
from calendar import monthrange
from typing import Dict
from typing import List
from typing import Tuple
import numpy as np

import pandas as pd
import datetime
from domino import Domino
import os

from assetallocation_arp.data_etl.dal.arp_proc_caller import TimesProcCaller
from assetallocation_arp.common_libraries.dal_enums.strategy import Name
from assetallocation_arp.common_libraries.dal_enums.fund_strategy import Signal, Performance
from assetallocation_arp.data_etl.dal.data_frame_converter import DataFrameConverter
from assetallocation_arp.data_etl.inputs_effect.find_date import find_date


class TimesChartsDataComputations(object):
    """Class doing computations for the data of the times dashboard"""

    def __init__(self):
        self.signals = None
        self.positions = None
        self.returns = None

        self._signals_comp = None
        self._positions_comp = None
        self._returns_comp = None
        self._returns_ytd = None

        self.positions_sum_start_date = None
        self.positions_start_date = None
        self.positions_end_date = None


    @property
    def signal_as_off(self) -> datetime:
        return self.signals.last_valid_index().strftime('%d-%m-%Y')

    @property
    def positions_sum_start_date(self) -> str:
        return self._positions_sum_start_date

    @positions_sum_start_date.setter
    def positions_sum_start_date(self, value: str) -> None:
        if value is None:
            value = '14-08-2018'
        self._positions_sum_start_date = value

    @property
    def positions_start_date(self) -> str:
        return self._positions_start_date

    @positions_start_date.setter
    def positions_start_date(self, value: str) -> None:
        if value is None:
            value = '15/05/2018'
        if self.positions is not None:
            value = find_date(self.positions.index.tolist(), pd.to_datetime(value, format='%d/%m/%Y'))
        self._positions_start_date = value

    @property
    def positions_end_date(self) -> str:
        return self._positions_end_date

    @positions_end_date.setter
    def positions_end_date(self, value: str) -> None:
        if value is None:
            value = '25/08/2018'
        if self.positions is not None:
            value = find_date(self.positions.index.tolist(), pd.to_datetime(value, format='%d/%m/%Y'))
        self._positions_end_date = value

    @property
    def positions_assets_length(self):
        return len(self.positions.loc[pd.to_datetime(self.positions_sum_start_date, format='%d-%m-%Y'):])

    def call_times_proc_caller(self, fund_name: str, version_strategy: int, date_from_sidebar=None, date_to_sidebar=None) -> None:
        """
        Call Times proc caller to grab the data from the db
        :param fund_name: name of the current fund (example: f1, f2,...)
        :param version_strategy: version of the current strategy (version1, version2, ...)
        :param date_from_sidebar: date from sidebar
        :param date_to_sidebar: date to sidebar
        :return: None
        """
        apc = TimesProcCaller()
        fs = apc.select_fund_strategy_results(fund_name, Name.times, version_strategy)
        weight_df = DataFrameConverter.fund_strategy_asset_weights_to_df(fs.asset_weights)
        analytic_df = DataFrameConverter.fund_strategy_asset_analytics_to_df(fs.analytics)

        self.signals = analytic_df.xs(Signal.momentum, level='analytic_subcategory')
        self.returns = analytic_df.xs(Performance['excess return'], level='analytic_subcategory')
        self.positions = weight_df

        if date_from_sidebar and date_to_sidebar is not None:
            self.signals = self.signals.loc[date_from_sidebar:date_to_sidebar]
            self.returns = self.returns.loc[date_from_sidebar:date_to_sidebar]
            self.positions = self.positions.loc[date_from_sidebar:date_to_sidebar]

    @staticmethod
    def call_domino_object():
        domino = Domino(
            "{domino_username}/{domino_project_name}".format(domino_username=os.environ['DOMINO_STARTING_USERNAME'],
                                                             domino_project_name=os.environ['DOMINO_PROJECT_NAME']),
            api_key=os.environ['DOMINO_USER_API_KEY'],
            host=os.environ['DOMINO_API_HOST'])

        return domino

    def export_times_data_to_csv(self, version):
        domino = self.call_domino_object()

        domino.files_upload("/signals_times_version{version}.csv".format(version=version), self.signals.to_csv())
        domino.files_upload("/returns_times_version{version}.csv".format(version=version), self.returns.to_csv())
        domino.files_upload("/positions_times_version{version}.csv".format(version=version), self.positions.to_csv())

    def export_times_positions_data_to_csv(self):

        domino = self.call_domino_object()
        domino.files_upload("/positions_charts_times_version.csv", self.positions.to_csv())

    @staticmethod
    def sort_by_category_assets(values_dict: dict, category_name: list):
        """
        Function which sorts the assets by category (Equities, Bonds, Forex)
        :param values_dict: values of assets
        :param category_name: Equities or Forex or Bonds
        :return: a dictionary
        """
        df = pd.DataFrame(values_dict.items(), columns=['Assets', 'Values'])
        df['Category'] = category_name
        # Assets
        assets = df.loc[df['Category'] == 'Equities'].Assets.tolist()
        fx = df.loc[df['Category'] == 'FX'].Assets.tolist()
        bonds = df.loc[df['Category'] == 'Bonds'].Assets.tolist()
        assets.extend(fx)
        assets.extend(bonds)
        # Category
        category = df.loc[df['Category'] == 'Equities'].Category.tolist()
        category_fx = df.loc[df['Category'] == 'FX'].Category.tolist()
        category_bonds = df.loc[df['Category'] == 'Bonds'].Category.tolist()
        category.extend(category_fx)
        category.extend(category_bonds)
        # Values of these assets
        values = df.loc[df['Category'] == 'Equities'].Values.tolist()
        values_fx = df.loc[df['Category'] == 'FX'].Values.tolist()
        values_bond = df.loc[df['Category'] == 'Bonds'].Values.tolist()
        values.extend(values_fx)
        values.extend(values_bond)

        return {'values': [val * 100 for val in values], 'assets': assets, 'category': category}

    @staticmethod
    def compute_trade_positions_all_assets_overview(delta: list) -> List[str]:
        """
        Compute the trade for each asset
        :return: a list with trades for each asset
        """
        return ['SELL' if val < 0 else 'BUY' for val in delta]

    @staticmethod
    def compute_ninety_fifth_percentile(assets_values: pd.DataFrame) -> float:
        """
        Compute  the 95th percentile
        :param assets_values: positions assets
        :return: a float
        """
        return np.percentile(assets_values, 95)

    @staticmethod
    def compute_fifth_percentile(assets_values: pd.DataFrame) -> float:
        """
        Compute the 5th percentile
        :param assets_values: positions of assets
        :return: a float
        """
        return np.percentile(assets_values, 5)

    @staticmethod
    def zip_results_performance_all_assets_overview(results_performance: dict):
        """
        Function zipping performances results
        :param results_performance: dict with all assets performances
        :return: a zip list
        """
        print(list(zip(*results_performance.values())))
        return zip(*results_performance.values())

    @staticmethod
    def round_results_all_assets_overview(results: list) -> List[float]:
        """
        Function rounding any results to 4
        :param results: list of results that should be round up
        :return: rounded list
        """
        return np.around(results, 4)

    @staticmethod
    def classify_assets_by_category(names_assets: list, values_perf=None) -> Tuple[List[str], Dict[str, float]]:
        """
        Function which classifies the assets per category
        :param names_assets: names of assets (Equities, FX, Bonds)
        :param values_perf: performance of assets in each category
        :return: a sorted list of categories and a dict with perf values depending on the category
        """
        category_name, perf_dict = [], {}
        for name in range(len(names_assets)):
            perf_dict[names_assets[name]] = values_perf[name]
            if 'Equities' in names_assets[name]:   # TODO improve it with Jess category from db?
                category_name.append('Equities')
            elif 'Bonds' in names_assets[name]:
                category_name.append('Bonds')
            else:
                category_name.append('FX')

        return category_name, perf_dict

    def build_percentile_list(self, assets_percentile: list) -> List[float]:
        """
        Function which build a list of percentile
        :param assets_percentile: percentile result
        :return: a list of percentile
        """
        return [assets_percentile] * self.positions_assets_length

    def compute_weekly_performance_all_assets_overview(self) -> Dict[str, List[float]]:
        """
        Compute the weekly performance for each assets
        :return:
        """
        # If statement with weekly only weekly?
        last_date = self.returns.index.get_loc(self.returns.last_valid_index()) - 1
        before_last_date = self.returns.index[last_date]
        prev_7_days_date = before_last_date - datetime.timedelta(days=7)

        v1 = self.returns.loc[before_last_date]
        v2 = self.returns.loc[prev_7_days_date]

        weekly_perf = (v1 - v2).apply(lambda x: x * 100)

        names_weekly_perf = weekly_perf.index.to_list()
        values_weekly_perf = weekly_perf.to_list()

        category_name,  weekly_perf_dict, = self.classify_assets_by_category(names_weekly_perf, values_weekly_perf)

        sort_weekly_perf = self.sort_by_category_assets(weekly_perf_dict, category_name)

        return {'weekly_performance_all_currencies': self.round_results_all_assets_overview(sort_weekly_perf['values']),
                'assets': sort_weekly_perf['assets'], 'category': sort_weekly_perf['category']}

    def compute_ytd_performance_all_assets_overview(self) -> Dict[str,  List[float]]:
        """
        Compute the YTD performance for each asset
        :return: a list with ytd performance for each asset
        """
        # Find out the last before last date
        last_date = self.returns.index.get_loc(self.returns.last_valid_index()) - 1
        before_last_date = self.returns.index[last_date]
        # Find the first date of the year
        days = []
        first_day_of_year = before_last_date - offsets.YearBegin()
        y, m = first_day_of_year.year, first_day_of_year.month
        for d in range(1, monthrange(y, m)[1] + 1):
            current_date = pd.to_datetime('{:02d}-{:02d}-{:04d}'.format(d, m, y), format='%d-%m-%Y')
            # We are checking if the first day of the year is not a weekend
            if current_date.weekday() <= 4:
                days.append(current_date)

        v1 = self.returns.loc[before_last_date]
        v2 = self.returns.loc[days[0]]

        ytd_perf = (v1 - v2).apply(lambda x: x * 100)

        names_ytd_perf = ytd_perf.index.to_list()
        values_ytd_perf = ytd_perf.to_list()

        category_name, ytd_perf_dict = self.classify_assets_by_category(names_ytd_perf, values_ytd_perf)

        sort_ytd_perf = self.sort_by_category_assets(ytd_perf_dict, category_name)
        return {'ytd_performance_all_currencies': self.round_results_all_assets_overview(sort_ytd_perf['values'])}

    def compute_mom_signals_all_assets_overview(self) -> np.ndarray:
        """
        Compute the Mom signals for each asset
        :return: a list with signals for each asset
        """
        # Find out the last date
        last_date = self.signals.last_valid_index()

        return self.round_results_all_assets_overview(self.signals.loc[last_date].values.tolist())

    def compute_previous_positions_all_assets_overview(self, strategy_weight: float) -> np.ndarray:
        """
        Compute the previous positions for each asset
        :return: a list with previous positions for each asset
        """
        # Find out the date of 7 days ago
        last_date = self.positions.index.get_loc(self.positions.last_valid_index())-1
        before_last_date = self.returns.index[last_date]
        prev_7_days_date = before_last_date - datetime.timedelta(days=7)

        return self.round_results_all_assets_overview(self.positions.loc[prev_7_days_date].apply(lambda x: (x * (1 + strategy_weight)) * 100).tolist())

    def compute_implemented_weight_overview(self):
        """
        Compute the implemented weight for each asset at the latest date
        :return: a list with the latest positions for each asset
        """

        # Find out the last date
        last_date = self.positions.last_valid_index()

        return self.round_results_all_assets_overview(self.positions.loc[last_date].tolist())

    def compute_new_positions_all_assets_overview(self, strategy_weight: float) -> np.ndarray:
        """
        Compute the new positions for each asset
        :return: a list with new positions for each asset
        """
        # Find out the last date
        last_date = self.positions.last_valid_index()

        return self.round_results_all_assets_overview(self.positions.loc[last_date].apply(lambda x: (x * (1 + strategy_weight)) * 100).tolist())

    def compute_delta_positions_all_assets_overview(self, prev_positions: pd.DataFrame, new_positions: pd.DataFrame)-> np.ndarray:
        """
        Compute the delta for each asset
        :return: a list with delta for each asset
        """
        return self.round_results_all_assets_overview(np.subtract(new_positions, prev_positions))

    def compute_size_positions_all_assets_overview(self, values: list, names: list, category_name: list, new_overall: pd.DataFrame) -> np.ndarray:
        """
        Function computing the size of each assets
        :param values:
        :param names:
        :param category_name:
        :param new_overall:
        :return: a list of size for each asset
        """
        df = pd.DataFrame(values, columns=['Values'])
        df['Assets'] = names
        df['Category'] = category_name

        equities = (df.loc[df['Category'] == 'Equities', 'Values'] / new_overall[0]).tolist()
        forex = (df.loc[df['Category'] == 'FX', 'Values'] / new_overall[1]).tolist()
        bonds = (df.loc[df['Category'] == 'Bonds', 'Values'] / new_overall[2]).tolist()

        size = []

        size.extend(equities + forex + bonds)

        return self.round_results_all_assets_overview(size)

    def compute_overall_performance_all_assets_overview(self, values: list, names: list, category_name: list) -> np.ndarray:
        """
        Function whic computes the performance for each asset
        :param values:
        :param names:
        :param category_name:
        :return: a list of performance depending on the category
        """
        df = pd.DataFrame(values, columns=['Values'])
        df['Assets'] = names
        df['Category'] = category_name

        return self.round_results_all_assets_overview([df.loc[df['Category'] == 'Equities', 'Values'].sum(),
                                                       df.loc[df['Category'] == 'FX', 'Values'].sum(),
                                                       df.loc[df['Category'] == 'Bonds', 'Values'].sum(),
                                                       df.Values.sum()])

    def compute_sum_positions_assets_charts(self, strategy_weight: float, start_date: str) -> Dict[str, List[float]]:
        """
        Function which computes the positions of each asset
        :param strategy_weight: weight of te strategy (0.46 as example)
        :param start_date: start date of positions assets
        :return: a ditionary with positions for each asset
        """
        equities_names, bonds_names, forex_names = [], [], []
        names = self.positions.columns.to_list()

        for name in names:
            if 'Equities' in name:
                equities_names.append(name)
            elif 'Bonds' in name:
                bonds_names.append(name)
            else:
                forex_names.append(name)

        # Start date of positions
        self.positions_sum_start_date = start_date
        equities = self.positions.loc[pd.to_datetime(self.positions_sum_start_date, format='%d-%m-%Y'):, equities_names]
        bonds = self.positions.loc[pd.to_datetime(self.positions_sum_start_date, format='%d-%m-%Y'):, bonds_names]
        forex = self.positions.loc[pd.to_datetime(self.positions_sum_start_date, format='%d-%m-%Y'):, forex_names]

        dates_positions_assets = equities.index.strftime("%Y-%m-%d").to_list()

        equities = equities.apply(lambda x: x * strategy_weight).sum(axis=1).tolist()
        bonds = bonds.apply(lambda x: x * strategy_weight).sum(axis=1).tolist()
        forex = forex.apply(lambda x: x * strategy_weight).sum(axis=1).tolist()

        return {'equities_pos_sum': equities, 'bonds_pos_sum': bonds, 'forex_pos_sum': forex,
                "dates_positions_assets": dates_positions_assets}

    def compute_positions_assets(self, start_date: str, end_date: str) -> Tuple[List[float], List[float], List[float]]:
        """
        Process positions depending on start and end date, selected by the user on the dashboard
        :param start_date: start date of positions
        :param end_date: end date of positions
        :return:
        """
        positions, sparklines_pos = [], []

        # Start and end dates positions
        self.positions_start_date, self.positions_end_date = start_date, end_date
        columns = self.positions.columns.tolist()
        names_pos = self.positions.columns.tolist()

        for col in columns:
            positions.append(self.positions.loc[self.positions_start_date:self.positions_end_date, col].to_list())
            sparklines_pos.append(self.positions[col].to_list())

        dates_pos = [self.positions.loc[self.positions_start_date:self.positions_end_date].index.strftime("%Y-%m-%d").to_list()]
        return positions, dates_pos, names_pos

    @staticmethod
    def build_dict_ready_for_zip(*results, keys: list) -> Dict[str, List[float]]:
        return {keys[key]: results[key] for key in range(len(keys))}

