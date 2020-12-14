from datetime import timedelta, datetime
from pandas.tseries import offsets
from calendar import monthrange
from typing import Dict
from typing import List
import numpy as np

import pandas as pd
import datetime

from assetallocation_arp.common_libraries.dal_enums.asset import Equity, FixedIncome, FX

# from assetallocation_UI.aa_web_app.data_import.compute_charts_data import TimesChartsDataComputations
from assetallocation_arp.data_etl.dal.arp_proc_caller import TimesProcCaller
from assetallocation_arp.common_libraries.dal_enums.strategy import Name
from assetallocation_arp.common_libraries.dal_enums.fund_strategy import Signal, Performance
from assetallocation_arp.data_etl.dal.data_frame_converter import DataFrameConverter


class TimesChartsDataComputations(object):
    """Class doing computations for the data of the times dashboard"""

    # def __init__(self, times_signals, times_positions, times_returns):
    def __init__(self):
        self.signals = None
        self.positions = None
        self.returns = None

        self._signals_comp = None
        self._positions_comp = None
        self._returns_comp = None
        self._returns_ytd = None

    @property
    def signal_as_off(self):
        return self.signals.last_valid_index().strftime("%d-%m-%Y")

    # @property
    # def max_signals_date(self) -> datetime:
    #     return self.signals.last_valid_index()
    #
    # @property
    # def max_returns_date(self) -> datetime:
    #     return self.returns.last_valid_index()
    #
    # @property
    # def max_positions_date(self) -> datetime:
    #     return self.positions.last_valid_index()
    #
    # @property
    # def returns_dates_weekly_off(self) -> datetime:
    #     return self.returns.last_valid_index().date() - timedelta(days=7)
    #
    # @property
    # def signals_comp(self) -> pd.DataFrame:
    #     return self._signals_comp
    #
    # @signals_comp.setter
    # def signals_comp(self, x: pd.DataFrame) -> None:
    #     self._signals_comp = x
    #
    # @property
    # def positions_comp(self) -> pd.DataFrame:
    #     return self._positions_comp
    #
    # @positions_comp.setter
    # def positions_comp(self, x: pd.DataFrame) -> None:
    #     self._positions_comp = x
    #
    # @property
    # def returns_comp(self) -> pd.DataFrame:
    #     return self._returns_comp
    #
    # @returns_comp.setter
    # def returns_comp(self, x: pd.DataFrame) -> None:
    #     self._returns_comp = x
    #
    # @property
    # def returns_ytd(self) -> pd.DataFrame:
    #     return self._returns_ytd
    #
    # @returns_ytd.setter
    # def returns_ytd(self, x: pd.DataFrame) -> None:
    #     self._returns_ytd = x
    #
    # @property
    # def positions_assets_length(self):
    #     #TODO change the date auto
    #     return len(self.positions.loc[pd.to_datetime('14-08-2018', format='%d-%m-%Y'):])

    def call_times_proc_caller(self, fund_name, version_strategy):
        apc = TimesProcCaller()
        fs = apc.select_fund_strategy_results(fund_name, Name.times, version_strategy)
        weight_df = DataFrameConverter.fund_strategy_asset_weights_to_df(fs.asset_weights)
        analytic_df = DataFrameConverter.fund_strategy_asset_analytics_to_df(fs.analytics)

        # data = {'times_signals': analytic_df.xs(Signal.momentum, level='analytic_subcategory'),
        #         'times_returns': analytic_df.xs(Performance['excess return'], level='analytic_subcategory'),
        #         'times_positions': weight_df}

        self.signals = analytic_df.xs(Signal.momentum, level='analytic_subcategory')
        self.returns = analytic_df.xs(Performance['excess return'], level='analytic_subcategory')
        self.positions = weight_df

    @staticmethod
    def sort_by_category_assets(weekly_perf_dict, category_name):
        df = pd.DataFrame(weekly_perf_dict.items(), columns=['Assets', 'Values'])
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

        return [val * 100 for val in values], assets, category

    @staticmethod
    def compute_trade_positions_all_assets_overview(delta)-> List[str]:
        """
        Compute the trade for each asset
        :return: a list with trade for each asset
        """
        return ['SELL' if val < 0 else 'BUY' for val in delta]

    @staticmethod
    def compute_ninety_fifth_percentile(assets_values):
        """
        Compute  the 95th percentile
        :param assets_values: positions assets
        :return: a float
        """
        return np.percentile(assets_values, 95)

    @staticmethod
    def compute_fifth_percentile(assets_values):
        """
        Compute the 5th percentile
        :param assets_values: positions of assets
        :return: a float
        """
        return np.percentile(assets_values, 5)

    @staticmethod
    def zip_results_performance_all_assets_overview(results_performance):
        """
        Function zipping performances results
        :param results_performance:
        :return: a zip list
        """
        print(list(zip(*results_performance.values())))
        return zip(*results_performance.values())

    @staticmethod
    def round_results_all_assets_overview(results):
        """
        Function rounding any results to 4
        :param results:
        :return: rounded list
        """
        return np.around(results, 4)

    @staticmethod
    def classify_assets_by_category(names_assets, values_perf):
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

    def compute_weekly_performance_all_assets_overview(self):
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

        weekly_perf_dict, category_name = self.classify_assets_by_category(names_weekly_perf, values_weekly_perf)

        values, assets, category = self.sort_by_category_assets(weekly_perf_dict, category_name)
        return self.round_results_all_assets_overview(values), assets, weekly_perf_dict, category

    def compute_ytd_performance_all_assets_overview(self):
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

        ytd_perf_dict, category_name = self.classify_assets_by_category(names_ytd_perf, values_ytd_perf)

        values, assets, category = self.sort_by_category_assets(ytd_perf_dict, category_name)
        return self.round_results_all_assets_overview(values), assets, ytd_perf_dict, category

    def compute_mom_signals_all_assets_overview(self):
        """
        Compute the Mom signals for each asset
        :return: a list with signals for each asset
        """
        # Find out the last date
        last_date = self.signals.last_valid_index()

        return self.round_results_all_assets_overview(self.signals.loc[last_date].values.tolist())

    def compute_previous_positions_all_assets_overview(self, strategy_weight) -> List[float]:
        """
        Compute the previous positions for each asset
        :return: a list with previous positions for each asset
        """
        # Find out the date of 7 days ago
        last_date = self.positions.index.get_loc(self.positions.last_valid_index()) - 1
        before_last_date = self.returns.index[last_date]
        prev_7_days_date = before_last_date - datetime.timedelta(days=7)

        return self.round_results_all_assets_overview(self.positions.loc[prev_7_days_date].apply(lambda x: (x * (1 + strategy_weight)) * 100).tolist())

    def compute_new_positions_all_assets_overview(self, strategy_weight)-> List[float]:
        """
        Compute the new positions for each asset
        :return: a list with new positions for each asset
        """
        # Find out the last date
        last_date = self.positions.last_valid_index()

        return self.round_results_all_assets_overview(self.positions.loc[last_date].apply(lambda x: (x * (1 + strategy_weight)) * 100).tolist())

    def compute_delta_positions_all_assets_overview(self, prev_positions, new_positions)-> List[float]:
        """
        Compute the delta for each asset
        :return: a list with delta for each asset
        """
        return self.round_results_all_assets_overview(np.subtract(new_positions, prev_positions))

    def compute_size_positions_all_assets_overview(self, values, names, category_name, new_overall):
        df = pd.DataFrame(values, columns=['Values'])
        df['Assets'] = names
        df['Category'] = category_name

        equities = (df.loc[df['Category'] == 'Equities', 'Values'] / new_overall[0]).tolist()
        forex = (df.loc[df['Category'] == 'FX', 'Values'] / new_overall[1]).tolist()
        bonds = (df.loc[df['Category'] == 'Bonds', 'Values'] / new_overall[2]).tolist()

        size = []

        size.extend(equities + forex + bonds)

        return self.round_results_all_assets_overview(size)

    def compute_overall_performance_all_assets_overview(self, values, names, category_name):
        #TODO gather df into one function
        df = pd.DataFrame(values, columns=['Values'])
        df['Assets'] = names
        df['Category'] = category_name

        return self.round_results_all_assets_overview([df.loc[df['Category'] == 'Equities', 'Values'].sum(),
                                                       df.loc[df['Category'] == 'FX', 'Values'].sum(),
                                                       df.loc[df['Category'] == 'Bonds', 'Values'].sum(),
                                                       df.Values.sum()])

    def compute_positions_assets_charts(self, strategy_weight):
        equities_names, bonds_names, forex_names = [], [], []
        names = self.positions.columns.to_list()

        for name in names:
            if 'Equities' in name:
                equities_names.append(name)
            elif 'Bonds' in name:
                bonds_names.append(name)
            else:
                forex_names.append(name)

        equities = self.positions.loc[pd.to_datetime('14-08-2018', format='%d-%m-%Y'):, equities_names]
        bonds = self.positions.loc[pd.to_datetime('14-08-2018', format='%d-%m-%Y'):, bonds_names]
        forex = self.positions.loc[pd.to_datetime('14-08-2018', format='%d-%m-%Y'):, forex_names]

        dates_positions_assets = equities.index.strftime("%Y-%m-%d").to_list()

        equities = equities.apply(lambda x: x * strategy_weight).sum(axis=1).tolist()
        bonds = bonds.apply(lambda x: x * strategy_weight).sum(axis=1).tolist()
        forex = forex.apply(lambda x: x * strategy_weight).sum(axis=1).tolist()

        return {'equities_pos_sum': equities, 'bonds_pos_sum': bonds, 'forex_pos_sum': forex,
                "dates_positions_assets": dates_positions_assets}

    def build_percentile_list(self, assets_percentile):
        """
        Function which build a list of percentile
        :param assets_percentile: percentile result
        :return: a list of percentile
        """
        return [assets_percentile] * self.positions_assets_length

    def process_data_from_a_specific_date(self, start_date='2018-05-15', end_date='2020-08-25'):
        positions, sparklines_pos = [], []
        columns = self.positions.columns.tolist()
        index_start_date = pd.to_datetime(start_date, format='%Y-%m-%d')
        index_end_date = pd.to_datetime(end_date, format='%Y-%m-%d')
        names_pos = self.positions.columns.tolist()
        # names = {'US Equities': 'S&P 500', 'EU Equities': 'CAC40', 'HK Equities': 'HK', 'UK 10y Bonds': 'FTSE'}  # TODO to automate later

        for col in columns:
            positions.append(self.positions.loc[index_start_date:index_end_date, col].to_list())
            sparklines_pos.append(self.positions[col].to_list())
            # names_pos.append(names[col])

        dates_pos = [self.positions.loc[index_start_date:index_end_date].index.strftime("%Y-%m-%d").to_list()]
        return positions, dates_pos, names_pos, sparklines_pos

    def run_times_charts_data_computations(self, strategy_weight):

        weekly_performance_all_currencies, names_weekly_perf, weekly_perf_dict, category_name = self.compute_weekly_performance_all_assets_overview()
        ytd_performance_all_currencies, names_ytd_perf, ytd_perf_dict, category_name = self.compute_ytd_performance_all_assets_overview()
        positions, dates_pos, names_pos, sparklines_pos = self.process_data_from_a_specific_date()
        mom_signals = self.compute_mom_signals_all_assets_overview()

        previous_positions = self.compute_previous_positions_all_assets_overview(strategy_weight)
        new_positions = self.compute_new_positions_all_assets_overview(strategy_weight)

        delta_positions = self.compute_delta_positions_all_assets_overview(previous_positions, new_positions)
        trade_positions = self.compute_trade_positions_all_assets_overview(delta_positions)

        # TODO to improve
        weekly_overall = self.compute_overall_performance_all_assets_overview(weekly_performance_all_currencies, names_weekly_perf, category_name)
        ytd_overall = self.compute_overall_performance_all_assets_overview(ytd_performance_all_currencies, names_ytd_perf, category_name)
        pre_overall = self.compute_overall_performance_all_assets_overview(previous_positions, names_weekly_perf, category_name)
        new_overall = self.compute_overall_performance_all_assets_overview(new_positions, names_weekly_perf, category_name)

        size = self.compute_size_positions_all_assets_overview(new_positions, names_weekly_perf, category_name, new_overall)

        positions_assets_sum = self.compute_positions_assets_charts(strategy_weight)

        # Percentile 95th
        equities_ninety_five_perc = self.compute_ninety_fifth_percentile(positions_assets_sum['equities_pos_sum'])
        bonds_ninety_five_perc = self.compute_ninety_fifth_percentile(positions_assets_sum['bonds_pos_sum'])
        forex_ninety_five_perc = self.compute_ninety_fifth_percentile(positions_assets_sum['forex_pos_sum'])

        # Percentile 5th
        equities_fifth_perc = self.compute_fifth_percentile(positions_assets_sum['equities_pos_sum'])
        bonds_fifth_perc = self.compute_fifth_percentile(positions_assets_sum['bonds_pos_sum'])
        forex_fifth_perc = self.compute_fifth_percentile(positions_assets_sum['forex_pos_sum'])

        # Build percentile list for positions charts
        equities_ninety_five_percentile = self.build_percentile_list(equities_ninety_five_perc)
        bonds_ninety_five_percentile = self.build_percentile_list(bonds_ninety_five_perc)
        forex_ninety_five_percentile = self.build_percentile_list(forex_ninety_five_perc)

        equities_fifth_percentile = self.build_percentile_list(equities_fifth_perc)
        bonds_fifth_percentile = self.build_percentile_list(bonds_fifth_perc)
        forex_fifth_percentile = self.build_percentile_list(forex_fifth_perc)

        results_positions = {"category_name": category_name,
                             "names_weekly_perf": names_weekly_perf,
                             "mom_signals": mom_signals,
                             "prev_positions": previous_positions,
                             "new_positions": new_positions,
                             "delta_positions": delta_positions,
                             "trade_positions": trade_positions,
                             "size_positions": size}

        results_perf = {"weekly_performance_all_currencies": weekly_performance_all_currencies,
                        "ytd_performance_all_currencies": ytd_performance_all_currencies}

        results_positions_overall = {"category_name": ['Equities', 'FX', 'Bonds', 'Total'],
                                     "pre_overall": pre_overall, "new_overall": new_overall}

        results_perf_overall = {"weekly_overall": weekly_overall, "ytd_overall": ytd_overall}

        zip_results_pos = self.zip_results_performance_all_assets_overview(results_positions)
        zip_results_pos_overall = self.zip_results_performance_all_assets_overview(results_positions_overall)
        zip_results_perf = self.zip_results_performance_all_assets_overview(results_perf)
        zip_results_perf_overall = self.zip_results_performance_all_assets_overview(results_perf_overall)

        template_data = {"positions": positions, "dates_pos": dates_pos, "names_pos": names_pos,
                         "sparklines_pos": sparklines_pos, "weekly_overall": weekly_overall,
                         "signal_as_off": self.signal_as_off, "positions_assets_sum": positions_assets_sum,
                         "equities_fifth_percentile": equities_fifth_percentile,
                         "equities_ninety_five_percentile": equities_ninety_five_percentile,
                         "bonds_ninety_five_percentile": bonds_ninety_five_percentile,
                         "bonds_fifth_percentile": bonds_fifth_percentile,
                         "forex_ninety_five_percentile": forex_ninety_five_percentile,
                         "forex_fifth_percentile": forex_fifth_percentile,
                         "mom_signals": mom_signals.tolist(),
                         "prev_positions": previous_positions.tolist(),
                         "new_positions": new_positions.tolist(),
                         "assets_names": names_weekly_perf,
                         "weekly_performance_all_currencies": weekly_performance_all_currencies.tolist(),
                         "ytd_performance_all_currencies": ytd_performance_all_currencies.tolist(),
                         "pre_overall": pre_overall.tolist()}

        return template_data, zip_results_pos, zip_results_pos_overall, zip_results_perf, zip_results_perf_overall