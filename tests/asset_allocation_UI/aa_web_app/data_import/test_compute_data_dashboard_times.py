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

    def test_compute_new_positions_each_asset(self):

        new_positions, new_positions_lst = self.dashboard_times.compute_new_positions_each_asset()

        new_positions_origin = [1.13838481091723000,
                                0.01742838121181100,
                                0.01099132750740320,
                                0.00017014400554600,
                                -9.27913403721271000,
                                -8.56886104603326000,
                                -10.72822688395760000,
                                -8.69508128387332000,
                                0.22606966024410900,
                                -2.68033008239423000,
                                5.83143308043204000,
                                -1.02974219952317000,
                                7.29237994882077000]

        np.testing.assert_almost_equal(new_positions_lst, new_positions_origin, decimal=13)

    def test_compute_delta_positions_each_asset(self):

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

        new_positions_origin = [1.13838481091723000,
                                0.01742838121181100,
                                0.01099132750740320,
                                0.00017014400554600,
                                -9.27913403721271000,
                                -8.56886104603326000,
                                -10.72822688395760000,
                                -8.69508128387332000,
                                0.22606966024410900,
                                -2.68033008239423000,
                                5.83143308043204000,
                                -1.02974219952317000,
                                7.29237994882077000]

        delta_positions = self.dashboard_times.compute_delta_positions_each_asset(previous_origin, new_positions_origin)

        delta_origin = [-0.37033111693327800,
                        -0.12155188682702300,
                        0.01029545026497280,
                        0.00016411993340340,
                        -0.05229709087478110,
                        0.23110037452389000,
                        -1.99681045063767000,
                        -1.05173581667324000,
                        0.68672893993358000,
                        0.20621907550820900,
                        0.92201621792110700,
                        -3.08249057670344000,
                        0.64297290051248300]

        np.testing.assert_almost_equal(delta_positions, delta_origin, decimal=13)

