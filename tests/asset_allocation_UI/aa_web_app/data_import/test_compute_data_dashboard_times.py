import os
import unittest
import pandas as pd
import numpy as np

from assetallocation_UI.aa_web_app.data_import.compute_data_dashboard_times import ComputeDataDashboardTimes
from tests.asset_allocation_UI.aa_web_app.data_for_test import data_origin_dashboard as data_origin


class TestComputeDataDashboardTimes(unittest.TestCase):

    def setUp(self):
        signals = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data_for_test",
                                                           "signals.csv")), sep=',', engine='python')
        returns = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data_for_test",
                                                           "returns.csv")), sep=',', engine='python')
        positions = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data_for_test",
                                                             "positions.csv")), sep=',', engine='python')

        signals.index = pd.to_datetime(signals['business_date'])
        returns.index = pd.to_datetime(returns['business_date'])
        positions.index = pd.to_datetime(positions['business_date'])

        self.dashboard_times = ComputeDataDashboardTimes(signals=signals, returns=returns, positions=positions)
        self.dashboard_times.strategy_weight = 0.46

    def test_compute_mom_signals_each_asset(self):

        mom_signals = self.dashboard_times.compute_mom_signals_each_asset()

        np.testing.assert_almost_equal(data_origin.mom_signals_origin, mom_signals, decimal=14)

    def test_compute_previous_positions_each_asset(self):

        previous_positions, previous_positions_lst = self.dashboard_times.compute_previous_positions_each_asset()

        np.testing.assert_almost_equal(data_origin.previous_positions_origin, previous_positions_lst, decimal=14)

    def test_compute_new_positions_each_asset(self):

        new_positions, new_positions_lst = self.dashboard_times.compute_new_positions_each_asset()

        np.testing.assert_almost_equal( data_origin.new_positions_origin, new_positions_lst, decimal=13)

    def test_compute_delta_positions_each_asset(self):

        delta_positions = self.dashboard_times.compute_delta_positions_each_asset(data_origin.previous_positions_origin,
                                                                                  data_origin.new_positions_origin)

        np.testing.assert_almost_equal(data_origin.delta_origin, delta_positions, decimal=13)

    def test_compute_trade_positions_each_asset(self):

        trade = self.dashboard_times.compute_trade_positions_each_asset(data_origin.previous_positions_origin_dict,
                                                                        data_origin.new_positions_origin_dict)

        self.assertEqual(data_origin.trade_origin, trade)

    def test_compute_positions_performance_per_category(self):

        pos_previous_perf = self.dashboard_times.compute_positions_performance_per_category(data_origin.previous_positions_origin_dict)
        pos_new_perf = self.dashboard_times.compute_positions_performance_per_category(data_origin.new_positions_origin_dict)
        weekly_performance_per_category = self.dashboard_times.compute_positions_performance_per_category(data_origin.weekly_performance_per_category_origin_dict, True)
        ytd_performance_per_category = self.dashboard_times.compute_positions_performance_per_category(data_origin.ytd_performance_per_category_origin_dict, True)

        np.testing.assert_almost_equal(list(data_origin.pos_previous_perf_origin_dict.values()), list(pos_previous_perf.values()),
                                       decimal=13)
        np.testing.assert_almost_equal(list(data_origin.pos_new_perf_origin_dict.values()), list(pos_new_perf.values()),
                                       decimal=13)
        np.testing.assert_almost_equal(list(data_origin.weekly_perf_origin_dict.values()), list(weekly_performance_per_category.values()),
                                       decimal=13)
        np.testing.assert_almost_equal(list(data_origin.ytd_perf_origin_dict.values()), list(ytd_performance_per_category.values()),
                                       decimal=13)

    def test_compute_size_positions_each_asset(self):

        size = self.dashboard_times.compute_size_positions_each_asset(data_origin.new_positions_origin_dict,
                                                                      data_origin.pos_new_perf_origin_dict)

        np.testing.assert_almost_equal(data_origin.size_origin, size, decimal=13)

    def test_compute_weekly_performance_each_asset(self):

        weekly_performance, weekly_performance_lst = self.dashboard_times.compute_weekly_performance_each_asset()

        np.testing.assert_almost_equal(data_origin.weekly_perf_origin, weekly_performance_lst, decimal=14)

    def test_compute_ytd_performance_each_asset(self):

        ytd_performance, ytd_performance_lst = self.dashboard_times.compute_ytd_performance_each_asset()

        np.testing.assert_almost_equal(data_origin.ytd_perf_origin, ytd_performance_lst, decimal=14)

    def test_compute_positions_position_1y_each_asset(self):

        position_1y, dates_pos, position_1y_per_asset, position_1y_lst = self.dashboard_times.\
            compute_positions_position_1y_each_asset(start_date=None, end_date=None)

        positions_1y_origin = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data_for_test",
                                                          "positions_one_year.csv")), sep=',', engine='python')
        positions_1y_origin.index = pd.to_datetime(positions_1y_origin['business_date'])
        del positions_1y_origin['business_date']

        assets_names = list(positions_1y_origin.columns)

        for asset_name in range(len(assets_names)):
            tmp_value = list(positions_1y_origin.loc[:, assets_names[asset_name]].values)
            np.testing.assert_almost_equal(tmp_value, position_1y_lst[asset_name], decimal=14)

    def test_sum_positions_per_category(self):

        position_1y, dates_pos, position_1y_per_asset, position_1y_lst = self.dashboard_times.\
            compute_positions_position_1y_each_asset(start_date=None, end_date=None)

        sum_positions_1y_origin = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..",
                                              "data_for_test", "sum_positions_one_year.csv")), sep=',', engine='python')
        sum_positions_1y_origin.index = pd.to_datetime(sum_positions_1y_origin['business_date'])

        sum_positions_per_category = self.dashboard_times.sum_positions_each_asset_into_category(position_1y)

        for key_category, value_category in sum_positions_per_category.items():
            tmp_sum_positions = list(sum_positions_1y_origin.loc[:, key_category].values)
            np.testing.assert_almost_equal(tmp_sum_positions, value_category, decimal=14)

    def test_compute_percentile_per_category(self):

        sum_positions_1y_origin = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..",
                                              "data_for_test", "sum_positions_one_year.csv")), sep=',', engine='python')
        sum_positions_1y_origin.index = pd.to_datetime(sum_positions_1y_origin['business_date'])

        assets_names = list(sum_positions_1y_origin.columns)

        sum_positions_per_category = {}

        for asset_name in range(1, len(assets_names)):
            sum_positions_per_category[assets_names[asset_name]] = list(sum_positions_1y_origin.loc[:,
                                                                        assets_names[asset_name]].values)

        ninety_fifth_percentile_per_category = self.dashboard_times.compute_percentile_per_category(sum_positions_per_category,
                                                                                                    percentile=95)

        fifth_percentile_per_category = self.dashboard_times.compute_percentile_per_category(sum_positions_per_category,
                                                                                             percentile=5)

        np.testing.assert_almost_equal(list(data_origin.ninety_fifth_percentile_per_category_origin.values()),
                                       list(ninety_fifth_percentile_per_category.values()), decimal=14)

        np.testing.assert_almost_equal(list(data_origin.fifth_percentile_per_category_origin.values()),
                                       list(fifth_percentile_per_category.values()), decimal=14)
