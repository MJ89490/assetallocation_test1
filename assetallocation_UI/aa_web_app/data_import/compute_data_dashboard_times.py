import datetime
import numpy as np
import pandas as pd
from typing import Dict
from typing import List
from typing import Tuple
from calendar import monthrange
from pandas.tseries import offsets
from assetallocation_arp.common_libraries.dal_enums.asset import Category
from assetallocation_arp.data_etl.inputs_effect.find_date import find_date


class ComputeDataDashboardTimes:
    """Class doing computations for the data of the times dashboard"""

    def __init__(self, signals, returns, positions):
        self._signals = signals
        self._positions = positions
        self._returns = returns

        self._signals_comp = None
        self._positions_comp = None
        self._returns_comp = None
        self._returns_ytd = None

        self._positions_sum_start_date = None
        self.positions_start_date = None
        self.positions_end_date = None

    @property
    def get_signal_as_off(self) -> datetime:
        return self._signals.last_valid_index().strftime('%d-%m-%Y')

    @property
    def get_asset_names(self):
        asset_names_sorted = []
        asset_names = sorted(set(self._signals.asset_name.to_list()), key=self._signals.asset_name.to_list().index)

        for category in Category:
            for asset_name in asset_names:
                if category.name in self.get_asset_names_per_category[asset_name]:
                    asset_names_sorted.append(asset_name)

        return asset_names_sorted

    @property
    def get_asset_names_per_category_sorted(self):
        asset_names_per_category_sorted = []
        asset_names = sorted(set(self._signals.asset_name.to_list()), key=self._signals.asset_name.to_list().index)

        for category in Category:
            for asset_name in asset_names:
                if category.name in self.get_asset_names_per_category[asset_name]:
                    asset_names_per_category_sorted.append(category.name)

        return asset_names_per_category_sorted

    @property
    def get_asset_names_per_category(self):
        return dict(zip(self._positions.asset_name, self._positions.asset_subcategory))

    @property
    def positions_sum_start_date(self) -> str:
        return self._positions_sum_start_date

    @positions_sum_start_date.setter
    def positions_sum_start_date(self, value: str) -> None:
        if value is None:
            value = '02-12-2000'  #'14-08-2018'
        self._positions_sum_start_date = value

    @property
    def positions_start_date(self) -> str:
        return self._positions_start_date

    @positions_start_date.setter
    def positions_start_date(self, value: str) -> None:
        if value is None:
            value = '02/12/2000'     # '15/05/2018'
        if self._positions is not None:
            value = find_date(list(pd.to_datetime(self._positions.business_date)), pd.to_datetime(value, format='%d/%m/%Y'))
        self._positions_start_date = value

    @property
    def positions_end_date(self) -> str:
        return self._positions_end_date

    @positions_end_date.setter
    def positions_end_date(self, value: str) -> None:
        if value is None:
            value = '02/07/2001'     #'25/08/2018'
            # value = self._positions.last_valid_index()
        if self._positions is not None:
            # value = find_date(self._positions.index.tolist(), pd.to_datetime(value, format='%d/%m/%Y'))
            value = find_date(list(pd.to_datetime(self._positions.business_date)), pd.to_datetime(value, format='%d/%m/%Y'))
        self._positions_end_date = value

    @staticmethod
    def zip_results_performance_all_assets_overview(results_performance: dict):
        """
        Function zipping performances results
        :param results_performance: dict with all assets performances
        :return: a zip list
        """

        return zip(*results_performance.values())

    @staticmethod
    def round_results_all_assets_overview(results: list) -> List[float]:
        """
        Function rounding any results to 4
        :param results: list of results that should be round up
        :return: rounded list
        """

        return [round(d, 3) for d in results]

    @staticmethod
    def build_dict_ready_for_zip(*results, keys: list) -> Dict[str, List[float]]:
        return {keys[key]: results[key] for key in range(len(keys))}

    def compute_weekly_performance_each_asset(self) -> Tuple[Dict[str, Dict[str, float]], List[float]]:
        """
        Compute the weekly performance for each assets
        :return:
        """
        # If statement with weekly only weekly?
        last_day_signals = self._signals.last_valid_index() - datetime.timedelta(days=2)
        prev_7_days_date_signals = self._signals.last_valid_index() - datetime.timedelta(days=9)

        weekly_performance, tmp_weekly_performance = {}, {}
        weekly_performance_lst = []

        for category in Category:
            for asset_name in self.get_asset_names:
                if category.name in self.get_asset_names_per_category[asset_name]:
                    tmp_returns = self._returns.loc[self._returns.asset_name == asset_name]
                    v1 = tmp_returns.loc[last_day_signals].value
                    v2 = tmp_returns.loc[prev_7_days_date_signals].value

                    tmp_weekly_performance[asset_name] = round(float((v1 - v2) * 100), 3)
                    weekly_performance_lst.append(round(float((v1 - v2) * 100), 3))

            if bool(tmp_weekly_performance):
                weekly_performance[category.name] = tmp_weekly_performance
                tmp_weekly_performance = {}

        return weekly_performance, weekly_performance_lst

    def compute_ytd_performance_each_asset(self) -> Tuple[Dict[str, Dict[str, float]], List[float]]:
        """
        Compute the YTD performance for each asset
        :return: a list with ytd performance for each asset
        """

        last_day_signals = self._signals.last_valid_index() - datetime.timedelta(days=2)
        signal_off = last_day_signals

        # Find the first date of the year
        days = []
        first_day_of_year = signal_off - offsets.YearBegin()
        y, m = first_day_of_year.year, first_day_of_year.month
        for d in range(1, monthrange(y, m)[1] + 1):
            current_date = pd.to_datetime('{:02d}-{:02d}-{:04d}'.format(d, m, y), format='%d-%m-%Y')
            # We are checking if the first day of the year is not a weekend
            if current_date.weekday() <= 4:
                days.append(current_date)

        ytd_performance, tmp_ytd_performance = {}, {}
        ytd_performance_lst = []

        for category in Category:
            for asset_name in self.get_asset_names:
                if category.name in self.get_asset_names_per_category[asset_name]:
                    tmp_returns = self._returns.loc[self._returns.asset_name == asset_name]
                    v1 = tmp_returns.loc[last_day_signals].value
                    v2 = tmp_returns.loc[days[0]].value
                    weekly_perf = round(float((v1 - v2) * 100), 3)

                    tmp_ytd_performance[asset_name] = weekly_perf
                    ytd_performance_lst.append(weekly_perf)

            if bool(tmp_ytd_performance):
                ytd_performance[category.name] = tmp_ytd_performance
                tmp_ytd_performance = {}

        return ytd_performance, ytd_performance_lst

    def compute_mom_signals_each_asset(self) -> List[float]:
        """
        Compute the Mom signals for each asset
        :return: a list with signals for each asset
        """
        # Find out the last date
        last_day_signals = self._signals.last_valid_index()
        mom_signals = []

        for category in Category:
            for asset_name in self.get_asset_names:
                if category.name in self.get_asset_names_per_category[asset_name]:
                    tmp_signals = self._signals.loc[self._signals.asset_name == asset_name]
                    mom_signals.append(round(float(tmp_signals.loc[last_day_signals].value), 3))

        return mom_signals

    def compute_positions_position_1y_each_asset(self, strategy_weight: float, start_date: None, end_date: None) \
            -> Tuple[Dict[str, Dict[str, float]], List[str], List[List[float]]]:
        """
        Process positions depending on start and end date, selected by the user on the dashboard
        :param start_date: start date of positions
        :param end_date: end date of positions
        :param strategy_weight: weight of the strategy
        :return:
        """

        self._positions.index = pd.to_datetime(self._positions.business_date)

        # Start and end dates positions
        self.positions_start_date, self.positions_end_date = start_date, end_date

        position_1y, tmp_position_1y = {}, {}
        dates_position_1y, position_1y_lst = [], []

        for category in Category:
            for asset_name in self.get_asset_names:
                if category.name in self.get_asset_names_per_category[asset_name]:
                    tmp_positions = self._positions.loc[self._positions.asset_name == asset_name]
                    tmp_positions.index = pd.to_datetime(tmp_positions.business_date)

                    if len(dates_position_1y) == 0:
                        dates_position_1y = tmp_positions.loc[self.positions_start_date:self.positions_end_date].index.strftime("%Y-%m-%d").to_list()

                    tmp_position_1y[asset_name] = tmp_positions.loc[self._positions_start_date:
                                                                    self._positions_end_date].value.apply(lambda x: float(x) * (1 + strategy_weight)).to_list()
                    position_1y_lst.append(tmp_positions.loc[self._positions_start_date:
                                                             self._positions_end_date].value.apply(lambda x: float(x) * (1 + strategy_weight)).to_list())
            if bool(tmp_position_1y):
                position_1y[category.name] = tmp_position_1y
                tmp_position_1y = {}

        return position_1y, dates_position_1y, position_1y_lst

    def compute_previous_positions_each_asset(self, strategy_weight: float) -> Tuple[Dict[str, Dict[str, float]],
                                                                                     List[float]]:
        """
        Compute the previous positions for each asset
        :return: a list with previous positions for each asset
        """

        last_day_signals = self._signals.last_valid_index() - datetime.timedelta(days=7)

        previous_positions, tmp_previous_positions = {}, {}
        previous_positions_lst = []

        for category in Category:
            for asset_name in self.get_asset_names:
                if category.name in self.get_asset_names_per_category[asset_name]:
                    tmp_positions = self._positions.loc[self._positions.asset_name == asset_name]
                    tmp_previous_positions[asset_name] = float(tmp_positions.loc[last_day_signals].value) * \
                                                         (1 + strategy_weight)
                    previous_positions_lst.append(round(float(tmp_positions.loc[last_day_signals].value) *
                                                        (1 + strategy_weight), 3))

            if bool(tmp_previous_positions):
                previous_positions[category.name] = tmp_previous_positions
                tmp_previous_positions = {}

        return previous_positions, previous_positions_lst

    def compute_new_positions_each_asset(self, strategy_weight: float) -> Tuple[Dict[str, Dict[str, float]],
                                                                                List[float]]:
        """
        Compute the new positions for each asset
        :return: a list with new positions for each asset
        """

        last_day_signals = self._signals.last_valid_index()

        new_positions, tmp_new_positions = {}, {}
        new_positions_lst = []

        for category in Category:
            for asset_name in self.get_asset_names:
                if category.name in self.get_asset_names_per_category[asset_name]:
                    tmp_positions = self._positions.loc[self._positions.asset_name == asset_name]
                    last_day_signals = find_date(list(pd.to_datetime(self._positions.business_date)),
                                                 pd.to_datetime(last_day_signals, format='%d/%m/%Y'))
                    tmp_new_positions[asset_name] = float(tmp_positions.loc[last_day_signals].value) * \
                                                    (1 + strategy_weight)
                    new_positions_lst.append(round(float(tmp_positions.loc[last_day_signals].value) *
                                                   (1 + strategy_weight), 3))

            if bool(tmp_new_positions):
                new_positions[category.name] = tmp_new_positions
                tmp_new_positions = {}

        return new_positions, new_positions_lst

    @staticmethod
    def compute_delta_positions_each_asset(prev_positions: List[float], new_positions: List[float])-> List[float]:
        """
        Compute the delta for each asset
        :return: a list with delta for each asset
        """

        delta_positions = []

        for i in range(len(prev_positions)):
            delta_positions.append(round((prev_positions[i] - new_positions[i]) * 100, 4))

        return delta_positions

    def compute_trade_positions_each_asset(self, prev_positions: Dict[str, Dict[str, float]],
                                           new_positions: Dict[str, Dict[str, float]])-> List[str]:
        """
        Compute the trade for each asset
        :return: a dict with trades for each asset
        """

        trade = []

        for category in Category:
            try:
                tmp_previous = prev_positions[category.name]
                tmp_new = new_positions[category.name]
                for asset_name in self.get_asset_names:
                    if category.name in self.get_asset_names_per_category[asset_name]:
                        if (tmp_new[asset_name] - tmp_previous[asset_name]) * 100 > 0:
                            trade.append('BUY')
                        else:
                            trade.append('SELL')
            except KeyError:
                continue

        return trade

    @staticmethod
    def compute_size_positions_each_asset(new_positions: Dict[str, Dict[str, float]], new_positions_per_category:
                                          Dict[str, float]) -> List[float]:
        size_positions = []

        for category_key in new_positions.keys():
            new_positions_per_category_value = new_positions_per_category[category_key]
            tmp_new_positions = new_positions[category_key]

            for tmp_key, tmp_value in tmp_new_positions.items():

                size_positions.append(round(tmp_value / new_positions_per_category_value, 3))

        return size_positions

    @staticmethod
    def compute_positions_performance_per_category(positions_performance_per_category: Dict[str, Dict[str, float]],
                                                   performance=False) -> Dict[str, float]:

        positions_category, tmp_positions_category = {}, {}

        for category in Category:
            try:
                tmp_positions = positions_performance_per_category[category.name]

                positions_category[category.name] = round(sum(tmp_positions.values()), 3)

            except KeyError:
                continue

        if performance:
            positions_category['Total'] = round(sum(positions_category.values()), 3)

        return positions_category

    @staticmethod
    def sum_positions_each_asset_into_category(positions)->Dict[str, List[float]]:

        sum_positions_per_category = {}

        for key_positions in positions.keys():
            tmp_positions_per_asset = []

            tmp_positions_per_category = positions[key_positions]

            # 1.Add each asset into sublist
            for key_asset in tmp_positions_per_category:
                tmp_positions_per_asset.append(tmp_positions_per_category[key_asset])

            # 2.Compute the sum per asset
            tmp_sum_per_category = []
            sum = 0

            for j in range(len(tmp_positions_per_asset[0])):
                for i in range(len(tmp_positions_per_asset)):
                    sum += tmp_positions_per_asset[i][j]
                tmp_sum_per_category.append(sum)
                sum = 0

            sum_positions_per_category[key_positions] = tmp_sum_per_category

        return sum_positions_per_category

    @staticmethod
    def compute_percentile_per_category(sum_category_values: Dict[str, List[float]], percentile: float) -> \
            Dict[str, float]:

        percentile_per_category = {}

        for key_category in sum_category_values.keys():
            percentile_per_category[key_category] = np.percentile(sum_category_values[key_category], percentile)

        return percentile_per_category

    @staticmethod
    def build_percentile_list(category_percentile: Dict[str, float], length_lst: int) -> Dict[str, List[float]]:

        percentile_list_per_category = {}

        for key_category in category_percentile:
            percentile_list_per_category[key_category] = [category_percentile[key_category]] * length_lst

        return percentile_list_per_category
