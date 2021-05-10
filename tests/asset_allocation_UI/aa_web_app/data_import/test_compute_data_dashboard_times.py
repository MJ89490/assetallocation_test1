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

    def test_compute_trade_positions_each_asset(self):
        new_positions_origin = {'Equity': {'Hang Seng Index Future ': 1.13838481091723000,
                                           'S&P 500 Total Return': 0.01742838121181100,
                                           'EURO STOXX 50 Total Return': 0.01099132750740320,
                                           'TOPIX Total Return': 0.00017014400554600},

                                'Fixed Income': {'Canada 10y Future ': -9.27913403721271000,
                                                 'Gilt Future': -8.56886104603326000,
                                                 'ML 10y US Treasury Total Return Future': -10.72822688395760000,
                                                 'Bund Future': -8.69508128387332000},

                                'FX': {'AUD-USD X-RATE': 0.22606966024410900,
                                       'USD-CAD X-RATE': -2.68033008239423000,
                                       'EUR-GBP X-RATE': 5.83143308043204000,
                                       'EUR-USD X-RATE': -1.02974219952317000,
                                       'USD-JPY X-RATE': 7.29237994882077000}}

        previous_positions_origin = {'Equity': {'Hang Seng Index Future ': 1.50871592785051000,
                                                'S&P 500 Total Return': 0.13898026803883400,
                                                'EURO STOXX 50 Total Return': 0.00069587724243040,
                                                'TOPIX Total Return': 0.00000602407214260},

                                     'Fixed Income': {'Canada 10y Future ': -9.22683694633793000,
                                                      'Gilt Future': -8.79996142055715000,
                                                      'ML 10y US Treasury Total Return Future': -8.73141643331991000,
                                                      'Bund Future': -7.64334546720008000},

                                     'FX': {'AUD-USD X-RATE': -0.46065927968947200,
                                            'USD-CAD X-RATE': -2.88654915790244000,
                                            'EUR-GBP X-RATE': 4.90941686251093000,
                                            'EUR-USD X-RATE': 2.05274837718027000,
                                            'USD-JPY X-RATE': 6.64940704830829000}}

        trade_origin = ['SELL', 'SELL', 'BUY', 'BUY', 'SELL', 'BUY', 'SELL', 'SELL', 'BUY', 'BUY', 'BUY', 'SELL', 'BUY']

        trade = self.dashboard_times.compute_trade_positions_each_asset(previous_positions_origin, new_positions_origin)

        self.assertEqual(trade, trade_origin)

    def test_compute_positions_performance_per_category(self):

        previous_positions_per_category_origin = {'Equity': {'Hang Seng Index Future ': 1.508715927850510,
                                                    'S&P 500 Total Return': 0.138980268038834,
                                                    'EURO STOXX 50 Total Return': 0.000695877242430,
                                                    'TOPIX Total Return': 0.000006024072143},

                                         'Fixed Income': {'Canada 10y Future ': -9.226836946337930,
                                                          'Gilt Future': -8.799961420557150,
                                                          'ML 10y US Treasury Total Return Future': -8.731416433319910,
                                                          'Bund Future': -7.643345467200080},

                                         'FX': {'AUD-USD X-RATE': -0.460659279689472,
                                                'USD-CAD X-RATE': -2.886549157902440,
                                                'EUR-GBP X-RATE': 4.909416862510930,
                                                'EUR-USD X-RATE': 2.052748377180270,
                                                'USD-JPY X-RATE': 6.649407048308290}}

        new_positions_per_category_origin = {'Equity': {'Hang Seng Index Future ': 1.13838481091723000,
                                                    'S&P 500 Total Return': 0.01742838121181100,
                                                    'EURO STOXX 50 Total Return': 0.01099132750740320,
                                                    'TOPIX Total Return':  0.00017014400554600},

                                         'Fixed Income': {'Canada 10y Future ': -9.27913403721271000,
                                                          'Gilt Future': -8.56886104603326000,
                                                          'ML 10y US Treasury Total Return Future': -10.72822688395760000,
                                                          'Bund Future': -8.69508128387332000},

                                         'FX': {'AUD-USD X-RATE': 0.22606966024410900,
                                                'USD-CAD X-RATE': -2.68033008239423000,
                                                'EUR-GBP X-RATE': 5.83143308043204000,
                                                'EUR-USD X-RATE': -1.02974219952317000,
                                                'USD-JPY X-RATE': 7.29237994882077000}}

        weekly_performance_per_category_origin = {'Equity': {'Hang Seng Index Future ': 0.003838237350610,
                                           'S&P 500 Total Return': 0.000575963785970,
                                           'EURO STOXX 50 Total Return': 0.000000151238820,
                                           'TOPIX Total Return': 0.000000081161990},

                              'Fixed Income': {'Canada 10y Future ': 0.022833079798870,
                                               'Gilt Future': -0.003338507041780,
                                               'ML 10y US Treasury Total Return Future': 0.005000511745520,
                                               'Bund Future': -0.003801280455570},

                              'FX': {'AUD-USD X-RATE': -0.001633193929370,
                                     'USD-CAD X-RATE': 0.010824584565110,
                                     'EUR-GBP X-RATE': 0.037269041737450,
                                     'EUR-USD X-RATE': -0.026612304382150,
                                     'USD-JPY X-RATE': 0.005185683077610}}

        ytd_performance_per_category_origin = {'Equity': {'Hang Seng Index Future ': 0.003840595935980,
                                           'S&P 500 Total Return': 0.000318655936690,
                                           'EURO STOXX 50 Total Return': 0.000001368335240,
                                           'TOPIX Total Return': 0.000000109737460},

                           'Fixed Income': {'Canada 10y Future ': -0.006427162968330,
                                            'Gilt Future':  -0.004289402728430,
                                            'ML 10y US Treasury Total Return Future': -0.020849375446650,
                                            'Bund Future': 0.001234473510720},

                           'FX': {'AUD-USD X-RATE': 0.000752914694770,
                                  'USD-CAD X-RATE': 0.002973867817740,
                                  'EUR-GBP X-RATE': -0.007909693723330,
                                  'EUR-USD X-RATE': -0.006922632982750,
                                  'USD-JPY X-RATE': -0.014132720201350}}

        pos_previous_perf = self.dashboard_times.compute_positions_performance_per_category(previous_positions_per_category_origin)
        pos_new_perf = self.dashboard_times.compute_positions_performance_per_category(new_positions_per_category_origin)
        weekly_performance_per_category = self.dashboard_times.compute_positions_performance_per_category(weekly_performance_per_category_origin, True)
        ytd_performance_per_category = self.dashboard_times.compute_positions_performance_per_category(ytd_performance_per_category_origin, True)

        pos_previous_perf_origin = {'Equity': 1.64839809720391,
                                    'Fixed Income': -34.40156026741510,
                                    'FX': 10.26436385040760}

        pos_new_perf_origin = {'Equity': 1.16697466364199,
                               'Fixed Income': -37.27130325107690,
                               'FX': 9.63981040757952}

        weekly_perf_origin = {'Equity': 0.00441443353739,
                              'Fixed Income': 0.02069380404704,
                              'FX': 0.02503381106865,
                              'Total': 0.05014204865308}

        ytd_perf_origin = {'Equity': 0.00416072994537,
                           'Fixed Income': -0.03033146763269,
                           'FX': -0.02523826439492,
                           'Total': -0.05140900208224}

        np.testing.assert_almost_equal(list(pos_previous_perf_origin.values()), list(pos_previous_perf.values()),
                                       decimal=13)
        np.testing.assert_almost_equal(list(pos_new_perf_origin.values()), list(pos_new_perf.values()),
                                       decimal=13)
        np.testing.assert_almost_equal(list(weekly_perf_origin.values()), list(weekly_performance_per_category.values()),
                                       decimal=13)
        np.testing.assert_almost_equal(list(ytd_perf_origin.values()), list(ytd_performance_per_category.values()),
                                       decimal=13)

    def test_compute_size_positions_each_asset(self):

        new_positions_origin = {'Equity': {'Hang Seng Index Future ': 1.13838481091723000,
                                                    'S&P 500 Total Return': 0.01742838121181100,
                                                    'EURO STOXX 50 Total Return': 0.01099132750740320,
                                                    'TOPIX Total Return':  0.00017014400554600},

                                         'Fixed Income': {'Canada 10y Future ': -9.27913403721271000,
                                                          'Gilt Future': -8.56886104603326000,
                                                          'ML 10y US Treasury Total Return Future': -10.72822688395760000,
                                                          'Bund Future': -8.69508128387332000},

                                         'FX': {'AUD-USD X-RATE': 0.22606966024410900,
                                                'USD-CAD X-RATE': -2.68033008239423000,
                                                'EUR-GBP X-RATE': 5.83143308043204000,
                                                'EUR-USD X-RATE': -1.02974219952317000,
                                                'USD-JPY X-RATE': 7.29237994882077000}}

        pos_new_perf_origin = {'Equity': 1.16697466364199,
                               'Fixed Income': -37.27130325107690,
                               'FX': 9.63981040757952}

        size_origin = [97.55008796544610000,
                       1.49346697531711000,
                       0.94186513639469900,
                       0.01457992284211220,
                        24.89618883113410000,
                        22.99050555949010000,
                        28.78414744900990000,
                        23.32915816036590000,
                        2.34516707990809000,
                        -27.80480081109020000,
                        60.49323413919990000,
                        -10.68218311340970000,
                        75.64858270539190000]

        size = self.dashboard_times.compute_size_positions_each_asset(new_positions_origin, pos_new_perf_origin)

        np.testing.assert_almost_equal(size, size_origin, decimal=13)

    def test_compute_weekly_performance_each_asset(self):

        weekly_performance, weekly_performance_lst = self.dashboard_times.compute_weekly_performance_each_asset()

        weekly_perf_origin = [0.003838237350610,
                              0.000575963785970,
                              0.000000151238820,
                              0.000000081161990,
                              0.022833079798870,
                              -0.003338507041780,
                              0.005000511745520,
                              -0.003801280455570,
                              -0.001633193929370,
                              0.010824584565110,
                              0.037269041737450,
                              -0.026612304382150,
                              0.005185683077610]

        np.testing.assert_almost_equal(weekly_perf_origin, weekly_performance_lst, decimal=14)

    def test_compute_ytd_performance_each_asset(self):

        ytd_performance, ytd_performance_lst = self.dashboard_times.compute_ytd_performance_each_asset()

        ytd_perf_origin = [0.003840595935980,
                           0.000318655936690,
                           0.000001368335240,
                           0.000000109737460,
                           -0.006427162968330,
                           -0.004289402728430,
                           -0.020849375446650,
                           0.001234473510720,
                           0.000752914694770,
                           0.002973867817740,
                           -0.007909693723330,
                           -0.006922632982750,
                           -0.014132720201350]

        np.testing.assert_almost_equal(ytd_perf_origin, ytd_performance_lst, decimal=14)




