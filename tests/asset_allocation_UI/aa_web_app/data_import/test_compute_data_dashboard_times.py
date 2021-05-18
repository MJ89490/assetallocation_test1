import os
import unittest
import pandas as pd
import numpy as np

from assetallocation_UI.aa_web_app.data_import.compute_data_dashboard_times import ComputeDataDashboardTimes
from tests.asset_allocation_UI.aa_web_app.data_for_test import data_expected_dashboard_unit_tests as expected_data

SUM_POSITIONS_1Y_EXPECTED = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..",
                                        "data_for_test", "sum_positions_one_year.csv")), sep=',', engine='python')

SUM_POSITIONS_1Y_EXPECTED.index = pd.to_datetime(SUM_POSITIONS_1Y_EXPECTED['business_date'])

ASSETS_NAMES = list(SUM_POSITIONS_1Y_EXPECTED.columns)


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

        np.testing.assert_almost_equal(expected_data.mom_signals_expected, mom_signals, decimal=14)

    def test_compute_previous_positions_each_asset(self):

        previous_positions, previous_positions_lst = self.dashboard_times.compute_previous_positions_each_asset()

        np.testing.assert_almost_equal(expected_data.previous_positions_expected, previous_positions_lst, decimal=14)

    def test_compute_new_positions_each_asset(self):

        new_positions, new_positions_lst = self.dashboard_times.compute_new_positions_each_asset()

        np.testing.assert_almost_equal(expected_data.new_positions_expected, new_positions_lst, decimal=13)

    def test_compute_delta_positions_each_asset(self):

        delta_positions = self.dashboard_times.compute_delta_positions_each_asset(expected_data.previous_positions_expected,
                                                                                  expected_data.new_positions_expected)

        np.testing.assert_almost_equal(expected_data.delta_expected, delta_positions, decimal=13)

    def test_compute_trade_positions_each_asset(self):

        trade = self.dashboard_times.compute_trade_positions_each_asset(expected_data.previous_positions_expectec_dict,
                                                                        expected_data.new_positions_expected_dict)

        self.assertEqual(expected_data.trade_expected, trade)

    def test_compute_positions_performance_per_category_positions_previous_performance(self):

        pos_previous_perf = self.dashboard_times.compute_positions_performance_per_category(expected_data.previous_positions_expectec_dict)

        np.testing.assert_almost_equal(list(expected_data.pos_previous_perf_expected_dict.values()), list(pos_previous_perf.values()),
                                       decimal=13)

    def test_compute_positions_performance_per_category_positions_new_performance(self):

        pos_new_perf = self.dashboard_times.compute_positions_performance_per_category(expected_data.new_positions_expected_dict)

        np.testing.assert_almost_equal(list(expected_data.pos_new_perf_expected_dict.values()), list(pos_new_perf.values()),
                                       decimal=13)

    def test_compute_positions_performance_per_category_weekly_performance(self):

        weekly_performance_per_category = self.dashboard_times.compute_positions_performance_per_category(expected_data.
                                                                                                          weekly_performance_per_category_expcted_dict, True)

        np.testing.assert_almost_equal(list(expected_data.weekly_perf_expected_dict.values()), list(weekly_performance_per_category.values()),
                                       decimal=13)

    def test_compute_positions_performance_per_category_ytd_performance(self):

        ytd_performance_per_category = self.dashboard_times.compute_positions_performance_per_category(expected_data.
                                                                                                       ytd_performance_per_category_expected_dict, True)

        np.testing.assert_almost_equal(list(expected_data.ytd_perf_expected_dict.values()), list(ytd_performance_per_category.values()),
                                       decimal=13)

    def test_compute_size_positions_each_asset(self):

        size = self.dashboard_times.compute_size_positions_each_asset(expected_data.new_positions_expected_dict,
                                                                      expected_data.pos_new_perf_expected_dict)

        np.testing.assert_almost_equal(expected_data.size_expected, size, decimal=13)

    def test_compute_weekly_performance_each_asset(self):

        weekly_performance, weekly_performance_lst = self.dashboard_times.compute_weekly_performance_each_asset()

        np.testing.assert_almost_equal(expected_data.weekly_perf_expected, weekly_performance_lst, decimal=14)

    def test_compute_ytd_performance_each_asset(self):

        ytd_performance, ytd_performance_lst = self.dashboard_times.compute_ytd_performance_each_asset()

        np.testing.assert_almost_equal(expected_data.ytd_perf_expected, ytd_performance_lst, decimal=14)

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

        sum_positions_per_category = self.dashboard_times.sum_positions_each_asset_into_category(position_1y)

        for key_category, value_category in sum_positions_per_category.items():
            tmp_sum_positions = list(SUM_POSITIONS_1Y_EXPECTED.loc[:, key_category].values)
            np.testing.assert_almost_equal(tmp_sum_positions, value_category, decimal=14)

    def test_compute_ninety_fifth_percentile_per_category(self):

        sum_positions_per_category = {}

        for asset_name in range(1, len(ASSETS_NAMES)):
            sum_positions_per_category[ASSETS_NAMES[asset_name]] = list(SUM_POSITIONS_1Y_EXPECTED.loc[:,
                                                                        ASSETS_NAMES[asset_name]].values)

        ninety_fifth_percentile_per_category = self.dashboard_times.compute_percentile_per_category(sum_positions_per_category,
                                                                                                    percentile=95)

        np.testing.assert_almost_equal(list(expected_data.ninety_fifth_percentile_per_category_expected.values()),
                                       list(ninety_fifth_percentile_per_category.values()), decimal=14)

    def test_compute_fifth_percentile_per_category(self):

        sum_positions_per_category = {}

        for asset_name in range(1, len(ASSETS_NAMES)):
            sum_positions_per_category[ASSETS_NAMES[asset_name]] = list(SUM_POSITIONS_1Y_EXPECTED.loc[:,
                                                                        ASSETS_NAMES[asset_name]].values)

        fifth_percentile_per_category = self.dashboard_times.compute_percentile_per_category(sum_positions_per_category,
                                                                                             percentile=5)

        np.testing.assert_almost_equal(list(expected_data.fifth_percentile_per_category_expected.values()),
                                       list(fifth_percentile_per_category.values()), decimal=14)
