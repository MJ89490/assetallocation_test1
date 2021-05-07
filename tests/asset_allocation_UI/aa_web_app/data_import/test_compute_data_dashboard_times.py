import os
import unittest
import pandas as pd
import numpy as np

from assetallocation_UI.aa_web_app.data_import.compute_data_dashboard_times import ComputeDataDashboardTimes


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

        mom_signals_origin = [0.5237260661579510,
                              0.0077611647784328,
                              0.0048410202306533,
                              0.0000627030556264,
                              -0.9870589427140550,
                              -0.9387784535218720,
                              -0.9832100098299460,
                              -0.7996913274169200,
                              -0.0500557397890073,
                              0.3988586757732350,
                              -0.8978670676749980,
                              -0.6675329611998070,
                              -0.9999854433730320]

        np.testing.assert_almost_equal(mom_signals, mom_signals_origin, decimal=14)

    def test_compute_previous_positions_each_asset(self):

        previous_positions, previous_positions_lst = self.dashboard_times.compute_previous_positions_each_asset()

        previous_origin = [1.508715927850510,
                           0.138980268038834,
                           0.000695877242430,
                           0.000006024072143,
                           -9.226836946337930,
                           -8.799961420557150,
                           -8.731416433319910,
                           -7.643345467200080,
                           -0.460659279689472,
                           -2.886549157902440,
                           4.909416862510930,
                           2.052748377180270,
                           6.649407048308290]

        np.testing.assert_almost_equal(previous_positions_lst, previous_origin, decimal=14)
