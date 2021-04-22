import datetime
import numpy as np
import pandas as pd
from typing import Dict
from typing import List
from typing import Tuple
from calendar import monthrange
from pandas.tseries import offsets

from assetallocation_arp.common_libraries.dal_enums.strategy import Name
from assetallocation_arp.common_libraries.dal_enums.asset import Category
from assetallocation_arp.data_etl.inputs_effect.find_date import find_date
from assetallocation_arp.data_etl.dal.arp_proc_caller import TimesProcCaller
from assetallocation_arp.data_etl.dal.data_frame_converter import DataFrameConverter
from assetallocation_arp.common_libraries.dal_enums.fund_strategy import Signal, Performance


class ComputeDataDashboardTimes:
    """Class doing computations for the data of the times dashboard"""

    def __init__(self):
        self._signals = None
        self._positions = None
        self._returns = None

        self._signals_comp = None
        self._positions_comp = None
        self._returns_comp = None
        self._returns_ytd = None

        self._positions_sum_start_date = None
        self.positions_start_date = None
        self.positions_end_date = None

    @property
    def get_names_assets(self)->List[str]:
        if self._positions is None:
            pass
        else:
            return [name.replace(name, "Fixed Income") if name == "Nominal Bond" else name for name in
                    self._positions.columns.to_list()]

    @property
    def get_signal_as_off(self) -> datetime:
        return self._signals.last_valid_index().strftime('%d-%m-%Y')

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

    @property
    def positions_assets_length(self):
        return len(self._positions.loc[pd.to_datetime(self._positions_sum_start_date, format='%d-%m-%Y'):])

    def call_times_proc_caller(self, fund_name: str, version_strategy: int, date_to: datetime, date_to_sidebar=None) -> None:
        """
        Call Times proc caller to grab the data from the db
        :param fund_name: name of the current fund (example: f1, f2,...)
        :param version_strategy: version of the current strategy (version1, version2, ...)
        :param date_to_sidebar: date to sidebar
        :return: None
        """
        apc = TimesProcCaller()
        fs = apc.select_fund_strategy_results(fund_name, Name.times, version_strategy,
                                              business_date_from=datetime.datetime.strptime('01/01/2000', '%d/%m/%Y').date(),
                                              business_date_to=date_to
                                              )

        self._positions = DataFrameConverter.fund_strategy_asset_weights_to_df(fs.asset_weights)

        analytic_df = DataFrameConverter.fund_strategy_asset_analytics_to_df(fs.analytics)

        self._signals = analytic_df.loc[analytic_df['analytic_subcategory'] == 'momentum']
        self._signals.index = pd.to_datetime(self._signals['business_date'])
        self._returns = analytic_df.loc[analytic_df['analytic_subcategory'] == 'excess return']
        self._returns.index = pd.to_datetime(self._returns['business_date'])

        if date_to_sidebar is not None:
            self._signals = self._signals.loc[:date_to_sidebar]
            self._returns = self._returns.loc[:date_to_sidebar]
            self._positions = self._positions.loc[:date_to_sidebar]

    @staticmethod
    def compute_ninety_fifth_percentile(assets_values: List[float]) -> float:
        """
        Compute  the 95th percentile
        :param assets_values: positions assets
        :return: a float
        """
        return np.percentile(assets_values, 95)

    @staticmethod
    def compute_fifth_percentile(assets_values: List[float]) -> float:
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

        return zip(*results_performance.values())

    @staticmethod
    def round_results_all_assets_overview(results: list) -> List[float]:
        """
        Function rounding any results to 4
        :param results: list of results that should be round up
        :return: rounded list
        """

        return [round(d, 4) for d in results]

    @staticmethod
    def build_dict_ready_for_zip(*results, keys: list) -> Dict[str, List[float]]:
        return {keys[key]: results[key] for key in range(len(keys))}

    def classify_assets_by_category(self) -> List[str]:
        """
        Function which classifies the assets per category
        :param names_assets: names of assets (Equities, FX, Bonds)
        :param values_perf: performance of assets in each category
        :return: a sorted list of categories and a dict with perf values depending on the category
        """
        category_name = []

        for name in self.get_names_assets:
            for category in Category:
                if category.name in name:
                    category_name.append(category.name)

        return category_name

    def build_percentile_list(self, assets_percentile: float) -> List[float]:
        """
        Function which build a list of percentile
        :param assets_percentile: percentile result
        :return: a list of percentile
        """
        return [assets_percentile] * self.positions_assets_length

    def compute_weekly_performance_each_asset(self) -> Dict[str, Dict[str, float]]:
        """
        Compute the weekly performance for each assets
        :return:
        """
        # If statement with weekly only weekly?
        last_day_signals = self._signals.last_valid_index() - datetime.timedelta(days=2)
        prev_7_days_date_signals = self._signals.last_valid_index() - datetime.timedelta(days=9)

        weekly_performance, tmp_weekly_performance = {}, {}

        asset_names = sorted(set(self._signals.asset_name.to_list()), key=self._signals.asset_name.to_list().index)
        self._positions.loc[(self._positions.asset_subcategory == 'Nominal Bond'), 'asset_subcategory'] = 'Fixed Income'
        asset_names_per_category = dict(zip(self._positions.asset_name, self._positions.asset_subcategory))

        for category in Category:
            for asset_name in asset_names:
                if category.name in asset_names_per_category[asset_name]:
                    tmp_returns = self._returns.loc[self._returns.asset_name == asset_name]
                    v1 = tmp_returns.loc[last_day_signals].value
                    v2 = tmp_returns.loc[prev_7_days_date_signals].value
                    weekly_perf = float((v1 - v2) * 100)

                    tmp_weekly_performance[asset_name] = round(weekly_perf, 4)

            if bool(tmp_weekly_performance):
                weekly_performance[category.name] = tmp_weekly_performance
                tmp_weekly_performance = {}

        return weekly_performance

    def compute_ytd_performance_each_asset(self) -> Dict[str, Dict[str, float]]:
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

        asset_names = sorted(set(self._signals.asset_name.to_list()), key=self._signals.asset_name.to_list().index)
        self._positions.loc[(self._positions.asset_subcategory == 'Nominal Bond'), 'asset_subcategory'] = 'Fixed Income'
        asset_names_per_category = dict(zip(self._positions.asset_name, self._positions.asset_subcategory))

        for category in Category:
            for asset_name in asset_names:
                if category.name in asset_names_per_category[asset_name]:
                    tmp_returns = self._returns.loc[self._returns.asset_name == asset_name]
                    v1 = tmp_returns.loc[last_day_signals].value
                    v2 = tmp_returns.loc[days[0]].value
                    weekly_perf = float((v1 - v2) * 100)

                    tmp_ytd_performance[asset_name] = round(weekly_perf, 4)

            if bool(tmp_ytd_performance):
                ytd_performance[category.name] = tmp_ytd_performance
                tmp_ytd_performance = {}

        return ytd_performance

    def compute_mom_signals_each_asset(self) -> Dict[str, Dict[str, float]]:
        """
        Compute the Mom signals for each asset
        :return: a list with signals for each asset
        """
        # Find out the last date
        last_day_signals = self._signals.last_valid_index()

        mom_signals, tmp_mom_signals = {}, {}

        asset_names = sorted(set(self._signals.asset_name.to_list()), key=self._signals.asset_name.to_list().index)
        self._positions.loc[(self._positions.asset_subcategory == 'Nominal Bond'), 'asset_subcategory'] = 'Fixed Income'
        asset_names_per_category = dict(zip(self._positions.asset_name, self._positions.asset_subcategory))

        for category in Category:
            for asset_name in asset_names:
                if category.name in asset_names_per_category[asset_name]:
                    tmp_signals = self._signals.loc[self._signals.asset_name == asset_name]
                    tmp_mom_signals[asset_name] = round(float(tmp_signals.loc[last_day_signals].value), 4)

            if bool(tmp_mom_signals):
                mom_signals[category.name] = tmp_mom_signals
                tmp_mom_signals = {}

        return mom_signals

    def compute_positions_position_1y_each_asset(self, strategy_weight: float, start_date: None, end_date: None) \
            -> Tuple[Dict[str, Dict[str, float]], List[str]]:
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
        dates_position_1y = []

        asset_names = sorted(set(self._signals.asset_name.to_list()), key=self._signals.asset_name.to_list().index)
        self._positions.loc[(self._positions.asset_subcategory == 'Nominal Bond'), 'asset_subcategory'] = 'Fixed Income'
        asset_names_per_category = dict(zip(self._positions.asset_name, self._positions.asset_subcategory))

        for category in Category:
            for asset_name in asset_names:
                if category.name in asset_names_per_category[asset_name]:
                    tmp_positions = self._positions.loc[self._positions.asset_name == asset_name]
                    tmp_positions.index = pd.to_datetime(tmp_positions.business_date)

                    if len(dates_position_1y) == 0:
                        dates_position_1y = [tmp_positions.loc[self.positions_start_date:self.positions_end_date].
                                             index.strftime("%Y-%m-%d").to_list()]

                    tmp_position_1y[asset_name] = tmp_positions.loc[self._positions_start_date:
                                                                    self._positions_end_date].value.apply(lambda x: float(x) * (1 + strategy_weight)).to_list()

            if bool(tmp_position_1y):
                position_1y[category.name] = tmp_position_1y
                tmp_position_1y = {}

        return position_1y, dates_position_1y

    def compute_previous_positions_each_asset(self, strategy_weight: float) -> Dict[str, Dict[str, float]]:
        """
        Compute the previous positions for each asset
        :return: a list with previous positions for each asset
        """

        last_day_signals = self._signals.last_valid_index() - datetime.timedelta(days=7)

        previous_positions, tmp_previous_positions = {}, {}

        asset_names = sorted(set(self._signals.asset_name.to_list()), key=self._signals.asset_name.to_list().index)
        self._positions.loc[(self._positions.asset_subcategory == 'Nominal Bond'), 'asset_subcategory'] = 'Fixed Income'
        asset_names_per_category = dict(zip(self._positions.asset_name, self._positions.asset_subcategory))

        for category in Category:
            for asset_name in asset_names:
                if category.name in asset_names_per_category[asset_name]:
                    tmp_positions = self._positions.loc[self._positions.asset_name == asset_name]
                    tmp_previous_positions[asset_name] = float(tmp_positions.loc[last_day_signals].value) * \
                                                          (1 + strategy_weight)

            if bool(tmp_previous_positions):
                previous_positions[category.name] = tmp_previous_positions
                tmp_previous_positions = {}

        return previous_positions

    def compute_new_positions_each_asset(self, strategy_weight: float) -> Dict[str, Dict[str, float]]:
        """
        Compute the new positions for each asset
        :return: a list with new positions for each asset
        """

        last_day_signals = self._signals.last_valid_index()

        new_positions, tmp_new_positions = {}, {}

        asset_names = sorted(set(self._signals.asset_name.to_list()), key=self._signals.asset_name.to_list().index)
        self._positions.loc[(self._positions.asset_subcategory == 'Nominal Bond'), 'asset_subcategory'] = 'Fixed Income'
        asset_names_per_category = dict(zip(self._positions.asset_name, self._positions.asset_subcategory))

        for category in Category:
            for asset_name in asset_names:
                if category.name in asset_names_per_category[asset_name]:
                    tmp_positions = self._positions.loc[self._positions.asset_name == asset_name]
                    last_day_signals = find_date(list(pd.to_datetime(self._positions.business_date)),
                                                 pd.to_datetime(last_day_signals, format='%d/%m/%Y'))
                    tmp_new_positions[asset_name] = float(tmp_positions.loc[last_day_signals].value) * \
                                                    (1 + strategy_weight)

            if bool(tmp_new_positions):
                new_positions[category.name] = tmp_new_positions
                tmp_new_positions = {}

        return new_positions

    def compute_delta_positions_each_asset(self, prev_positions: Dict[str, Dict[str, float]], new_positions:
                                           Dict[str, Dict[str, float]])-> Dict[str, Dict[str, float]]:
        """
        Compute the delta for each asset
        :return: a list with delta for each asset
        """

        delta, tmp_delta = {}, {}

        asset_names = sorted(set(self._signals.asset_name.to_list()), key=self._signals.asset_name.to_list().index)
        self._positions.loc[(self._positions.asset_subcategory == 'Nominal Bond'), 'asset_subcategory'] = 'Fixed Income'
        asset_names_per_category = dict(zip(self._positions.asset_name, self._positions.asset_subcategory))

        for category in Category:
            try:
                tmp_previous = prev_positions[category.name]
                tmp_new = new_positions[category.name]
                for asset_name in asset_names:
                    if category.name in asset_names_per_category[asset_name]:
                        tmp_previous_asset_name = tmp_previous[asset_name]
                        tmp_new_asset_name = tmp_new[asset_name]

                        tmp_delta[asset_name] = (tmp_new_asset_name - tmp_previous_asset_name) * 100

                if bool(tmp_delta):
                    delta[category.name] = tmp_delta
                    tmp_delta = {}
            except KeyError:
                continue

        return delta

    def compute_trade_positions_each_asset(self, prev_positions: Dict[str, Dict[str, float]],
                                           new_positions: Dict[str, Dict[str, float]])-> Dict[str, Dict[str, float]]:
        """
        Compute the trade for each asset
        :return: a dict with trades for each asset
        """

        trade, tmp_trade = {}, {}

        asset_names = sorted(set(self._signals.asset_name.to_list()), key=self._signals.asset_name.to_list().index)
        self._positions.loc[(self._positions.asset_subcategory == 'Nominal Bond'), 'asset_subcategory'] = 'Fixed Income'
        asset_names_per_category = dict(zip(self._positions.asset_name, self._positions.asset_subcategory))

        for category in Category:
            try:
                tmp_previous = prev_positions[category.name]
                tmp_new = new_positions[category.name]
                for asset_name in asset_names:
                    if category.name in asset_names_per_category[asset_name]:
                        tmp_previous_asset_name = tmp_previous[asset_name]
                        tmp_new_asset_name = tmp_new[asset_name]

                        if (tmp_new_asset_name - tmp_previous_asset_name) * 100 > 0:
                            tmp_trade[asset_name] = 'BUY'
                        else:
                            tmp_trade[asset_name] = 'SELL'

                if bool(tmp_trade):
                    trade[category.name] = tmp_trade
                    tmp_trade = {}
            except KeyError:
                continue

        return trade

    def compute_positions_per_category(self, positions_per_category: Dict[str, Dict[str, float]]) -> Dict[str, float]:

        positions_category, tmp_positions_category = {}, {}

        self._positions.loc[(self._positions.asset_subcategory == 'Nominal Bond'), 'asset_subcategory'] = 'Fixed Income'

        for category in Category:
            try:
                tmp_positions = positions_per_category[category.name]

                positions_category[category.name] = sum(tmp_positions.values())
            except KeyError:
                continue

        return positions_category
































    def compute_size_positions_all_assets_overview(self, values: np.ndarray, new_overall: np.ndarray) -> np.ndarray:
        """
        Function computing the size of each assets
        :param values:
        :param names:
        :param category_name:
        :param new_overall:
        :return: a list of size for each asset
        """
        df = pd.DataFrame(values, columns=['Values'])
        df['Assets'] = self.get_names_assets
        df['Category'] = self.classify_assets_by_category()

        # equities = (df.loc[df['Category'] == 'Equity', 'Values'] / new_overall[0]).tolist()
        # forex = (df.loc[df['Category'] == 'FX', 'Values'] / new_overall[1]).tolist()
        # bonds = (df.loc[df['Category'] == 'Nominal Bond', 'Values'] / new_overall[2]).tolist()

        # size = []

        # size.extend(equities + forex + bonds)

        size = df.Values / new_overall[0:3]

        return self.round_results_all_assets_overview(size)



    def compute_sum_positions_assets_charts(self, strategy_weight: float, start_date: str) -> Dict[str, List[float]]:
        """
        Function which computes the positions of each asset
        :param strategy_weight: weight of te strategy (0.46 as example)
        :param start_date: start date of positions assets
        :return: a dictionary with positions for each asset
        """

        self.positions_sum_start_date = start_date

        self._positions.columns = [name.replace(name, 'Fixed Income') if name == 'Nominal Bond' else name for name
                                   in self._positions.columns]

        tmp_category,  category_sort = [], {}

        for category in Category:
            for name in self.get_names_assets:
                if category.name in name:
                    tmp_category.append(name)

            if len(tmp_category) != 0:
                category_sort[category.name] = self._positions.loc[pd.to_datetime(self._positions_sum_start_date,
                                                                                  format='%d-%m-%Y'):, tmp_category].apply(lambda x: x * strategy_weight).sum(axis=1).tolist()
            tmp_category = []

        category_sort['titles_ids'] = [key for key in category_sort.keys()]
        category_sort['dates_positions_assets'] = self._positions.index.strftime("%Y-%m-%d").to_list()

        return category_sort




if __name__ == "__main__":

    obj = ComputeDataDashboardTimes()
    obj.call_times_proc_caller("test_fund", 1066, datetime.datetime.strptime('08/08/2001', '%d/%m/%Y'), date_to_sidebar=None)

