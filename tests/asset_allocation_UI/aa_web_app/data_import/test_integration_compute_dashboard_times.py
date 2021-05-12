import os
import unittest
import numpy as np
import pandas as pd

from assetallocation_UI.aa_web_app.data_import.compute_data_dashboard_times import ComputeDataDashboardTimes
from assetallocation_UI.aa_web_app.data_import.main_compute_data_dashboard_times import main_compute_data_dashboard_times
from tests.asset_allocation_UI.aa_web_app.data_for_test import data_origin_dashboard_integration_test as data_origin


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

    def test_main_compute_data_dashboard_times(self):
        template_data = main_compute_data_dashboard_times(obj_charts_data=self.dashboard_times, start_date=None,
                                                          end_date=None)

        template_data_origin = data_origin.template_data_origin

        # dates_pos
        np.testing.assert_equal(template_data_origin["dates_pos"], template_data["dates_pos"])

        # mom_signals
        np.testing.assert_almost_equal(template_data_origin["mom_signals"], template_data["mom_signals"])

        # dates_pos_alloc
        np.testing.assert_equal(template_data_origin["dates_pos_alloc"], template_data["dates_pos_alloc"])

        # new_positions
        np.testing.assert_almost_equal(template_data_origin["new_positions"], template_data["new_positions"])

        # prev_positions
        np.testing.assert_almost_equal(template_data_origin["prev_positions"], template_data["prev_positions"])

        # pre_overall
        np.testing.assert_almost_equal(list(template_data_origin["pre_overall"].values()), list(template_data["pre_overall"].values()))

        # assets_names
        np.testing.assert_equal(template_data_origin["assets_names"], template_data["assets_names"])

        # weekly_overall
        np.testing.assert_almost_equal(list(template_data_origin["weekly_overall"].values()), list(template_data["weekly_overall"].values()))

        # signal_as_off
        np.testing.assert_equal(template_data_origin["signal_as_off"], template_data["signal_as_off"])

        # ytd_performance_all_currencies
        np.testing.assert_almost_equal(template_data_origin["ytd_performance_all_currencies"], template_data["ytd_performance_all_currencies"])

        # weekly_performance_all_currencies
        np.testing.assert_almost_equal(template_data_origin["weekly_performance_all_currencies"], template_data["weekly_performance_all_currencies"])