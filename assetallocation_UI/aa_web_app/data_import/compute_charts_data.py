from datetime import timedelta, datetime
from pandas.tseries import offsets
from calendar import monthrange
from typing import Dict
from typing import List
import numpy as np

import pandas as pd
import datetime

from assetallocation_arp.common_libraries.dal_enums.asset import Equity, FixedIncome, FX


class TimesChartsDataComputations(object):
    """Class doing computations for the data of the times dashboard"""

    def __init__(self, times_signals, times_positions, times_returns):
        self.signals = times_signals
        self.positions = times_positions
        self.returns = times_returns
        self._signals_comp = None
        self._positions_comp = None
        self._returns_comp = None
        self._returns_ytd = None

    @property
    def signal_as_off(self):

        return self.signals.last_valid_index().strftime("%d-%m-%Y")

    @property
    def max_signals_date(self) -> datetime:
        return self.signals.last_valid_index()

    @property
    def max_returns_date(self) -> datetime:
        return self.returns.last_valid_index()

    @property
    def max_positions_date(self) -> datetime:
        return self.positions.last_valid_index()

    @property
    def returns_dates_weekly_off(self) -> datetime:
        return self.returns.last_valid_index().date() - timedelta(days=7)

    # @property
    # def prev_year_end(self) -> datetime:
    #     return datetime(self.max_returns_date.year, 1, 1) - timedelta(1)

    @property
    def signals_comp(self) -> pd.DataFrame:
        return self._signals_comp

    @signals_comp.setter
    def signals_comp(self, x: pd.DataFrame) -> None:
        self._signals_comp = x

    @property
    def positions_comp(self) -> pd.DataFrame:
        return self._positions_comp

    @positions_comp.setter
    def positions_comp(self, x: pd.DataFrame) -> None:
        self._positions_comp = x

    @property
    def returns_comp(self) -> pd.DataFrame:
        return self._returns_comp

    @returns_comp.setter
    def returns_comp(self, x: pd.DataFrame) -> None:
        self._returns_comp = x

    @property
    def returns_ytd(self) -> pd.DataFrame:
        return self._returns_ytd

    @returns_ytd.setter
    def returns_ytd(self, x: pd.DataFrame) -> None:
        self._returns_ytd = x

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

        weekly_perf_dict, category_name = {}, []
        # TODO to improve in order to not repeat code
        for name in range(len(names_weekly_perf)):
            weekly_perf_dict[names_weekly_perf[name]] = values_weekly_perf[name]
            if 'Equities' in names_weekly_perf[name]:   # TODO improve it with Jess category from db?
                category_name.append('Equities')
            elif 'Bonds' in names_weekly_perf[name]:
                category_name.append('Bonds')
            else:
                category_name.append('FX')

        values, assets, category = self.sort_by_category_assets(weekly_perf_dict, category_name)
        return self.round_results_all_assets_overview(values), assets, weekly_perf_dict, category

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

        return values, assets, category

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

        ytd_perf_dict, category_name = {}, []
        # TODO to put in a fct
        for name in range(len(names_ytd_perf)):
            ytd_perf_dict[names_ytd_perf[name]] = values_ytd_perf[name]
            if 'Equities' in names_ytd_perf[name]:   # TODO improve it with Jess category from db?
                category_name.append('Equities')
            elif 'Bonds' in names_ytd_perf[name]:
                category_name.append('Bonds')
            else:
                category_name.append('FX')

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

    @staticmethod
    def compute_trade_positions_all_assets_overview(delta)-> List[str]:
        """
        Compute the trade for each asset
        :return: a list with trade for each asset
        """

        return ['SELL' if val < 0 else 'BUY' for val in delta]

    @staticmethod
    def compute_size_positions_all_assets_overview():
        pass

    # TODO gather both function below into a single one
    def compute_weekly_ytd_overall_performance_all_assets_overview(self, values, names, category_name):

        df = pd.DataFrame(values, columns=['Values'])
        df['Assets'] = names
        df['Category'] = category_name

        return self.round_results_all_assets_overview([df.loc[df['Category'] == 'Equities', 'Values'].sum() * 100,
                                                       df.loc[df['Category'] == 'FX', 'Values'].sum() * 100,
                                                       df.loc[df['Category'] == 'Bonds', 'Values'].sum() * 100,
                                                      ])

    @staticmethod
    def zip_results_performance_all_assets_overview(results_performance):
        print(list(zip(*results_performance.values())))
        return zip(*results_performance.values())

    @staticmethod
    def round_results_all_assets_overview(results):
        return np.around(results, 4)

    @staticmethod
    def process_data_from_a_specific_date(times_data):
        positions, sparklines_pos = [], []
        columns = times_data.columns.tolist()
        index_start_date = pd.to_datetime('2018-05-15', format='%Y-%m-%d')
        names_pos = times_data.columns.tolist()
        # names = {'US Equities': 'S&P 500', 'EU Equities': 'CAC40', 'HK Equities': 'HK', 'UK 10y Bonds': 'FTSE'}  # TODO to automate later

        for col in columns:
            positions.append(times_data.loc[index_start_date:, col].to_list())
            sparklines_pos.append(times_data[col].to_list())
            # names_pos.append(names[col])

        dates_pos = [times_data.loc[index_start_date:].index.strftime("%Y-%m-%d").to_list()]
        return positions, dates_pos, names_pos, sparklines_pos





    # def data_computations(self) -> Dict[str, pd.DataFrame]:
    #     self.signals_comp = round(self.signals.loc[self.max_signals_date], 2)
    #     self.positions_comp = round(self.positions.loc[self.max_positions_date] * 100, 2)
    #     self.returns_comp = round((self.returns.loc[self.max_returns_date] - self.returns.loc[self.returns_dates_weekly_off]) * 100, 3)
    #     # self.returns_ytd = round((self.returns.loc[self.max_returns_date] - self.returns.loc[self.prev_year_end]) * 100, 3)
    #
    #     return {'times_signals_comp': self.signals_comp, 'times_positions_comp': self.positions_comp,
    #             'times_returns_comp': self.returns_comp, 'times_returns_ytd': self.returns_ytd}
    #
    # def data_computations_sum(self) -> Dict[str, pd.DataFrame]:
    #     """
    #     :return: dictionary with all the computations such as the sum of the equities positions, sum of the bonds positions
    #     """
    #     sum_positions_bonds, sum_positions_equities, sum_positions_fx = self.sum_equities_bonds_fx(self.positions_comp)
    #     sum_performance_weekly_equities, sum_performance_weekly_bonds, sum_performance_weekly_fx = self.sum_equities_bonds_fx(self.returns_comp)
    #     sum_performance_ytd_equities, sum_performance_ytd_bonds, sum_performance_ytd_fx = self.sum_equities_bonds_fx(self.returns_ytd)
    #
    #     return {'sum_positions_equities': sum_positions_equities, 'sum_positions_bonds': sum_positions_bonds,
    #             'sum_positions_fx': sum_positions_fx, 'sum_performance_weekly_equities': sum_performance_weekly_equities,
    #             'sum_performance_weekly_bonds': sum_performance_weekly_bonds, 'sum_performance_weekly_fx': sum_performance_weekly_fx,
    #             'sum_performance_ytd_equities': sum_performance_ytd_equities, 'sum_performance_ytd_bonds': sum_performance_ytd_bonds,
    #             'sum_performance_ytd_fx': sum_performance_ytd_fx}
    #
    # def sum_equities_bonds_fx(self, equities_bonds_fx_data):
    #     equities = [i.name for i in Equity if i.name in equities_bonds_fx_data.index]
    #     bonds = [i.name for i in FixedIncome if i.name in equities_bonds_fx_data.index]
    #     fx = [i.name for i in FX if i.name in equities_bonds_fx_data.index]
    #
    #     equities = self.round_sum(equities_bonds_fx_data.loc[equities])
    #     bonds = self.round_sum(equities_bonds_fx_data.loc[bonds])
    #     fx = self.round_sum(equities_bonds_fx_data.loc[fx])
    #     return bonds, equities, fx
    #
    # @staticmethod
    # def round_sum(df):
    #     return round(sum(df), 2)


