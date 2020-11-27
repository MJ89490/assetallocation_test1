import os
import pytest
import numpy as np
import pandas as pd
from unittest import TestCase

from assetallocation_arp.models.effect.compute_currencies import ComputeCurrencies
from data_etl.inputs_effect.compute_inflation_differential import ComputeInflationDifferential
from assetallocation_arp.models.effect.compute_profit_and_loss_overview import ComputeProfitAndLoss

"""
Notes: 
    TrendIndicator: Total Return
    Short-term: 4
    Long-term: 16 
    Incl Shorts: Yes
    Cut-off long: 2.0% 
    Cut-off short: 0.0% 
    Real/Nominal: real
    Realtime Inflation F'cast: Yes
    Threshold for closing: 0.25%
    Risk-weighting: 1/N
    STDev window (weeks): 52
    Bid-ask spread (bp): 10
    Position size: 3%
"""


class TestComputeProfitAndLoss(TestCase):

    def setUp(self):
        all_data = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "all_date.csv")), sep=',', engine='python')
        all_data = all_data.set_index(pd.to_datetime(all_data.Date, format='%Y-%m-%d'))
        del all_data['Date']
        self.obj_import_data = ComputeCurrencies(asset_inputs=pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "asset_inputs.csv")), sep=',', engine='python'),
                                                 bid_ask_spread=10,
                                                 frequency_mat='weekly',
                                                 end_date_mat='23/09/2020',
                                                 signal_day_mat='WED',
                                                 all_data=all_data)

        self.obj_import_data.process_all_data_effect()
        self.obj_import_data.start_date_calculations = pd.to_datetime('12-01-2000', format='%d-%m-%Y')

        # Inflation differential calculations
        obj_inflation_differential = ComputeInflationDifferential(dates_index=self.obj_import_data.dates_index)
        realtime_inflation_forecast, imf_data_update = 'Yes', False
        inflation_differential, currency_logs = obj_inflation_differential.compute_inflation_differential(
                                                realtime_inflation_forecast,
                                                self.obj_import_data.all_currencies_spot,
                                                self.obj_import_data.currencies_spot['currencies_spot_usd'],
                                                imf_data_update=imf_data_update)

        # Inputs
        trend_inputs = {'short_term': 4, 'long_term': 16, 'trend': 'total return'}
        carry_inputs = {'type': 'real', 'inflation': inflation_differential}
        combo_inputs = {'cut_off': 2, 'incl_shorts': 'Yes', 'cut_off_s': 0.00, 'threshold': 0.25}

        self.currencies_calculations = self.obj_import_data.run_compute_currencies(carry_inputs, trend_inputs, combo_inputs)

        self.obj_compute_profit_and_loss = ComputeProfitAndLoss(latest_date=pd.to_datetime('23-09-2020', format='%d-%m-%Y'),
                                                                position_size_attribution=0.03,
                                                                index_dates=self.obj_import_data.dates_origin_index,
                                                                frequency='weekly')

    def test_compute_profit_and_loss_combo(self):
        p_and_l_combo = self.obj_compute_profit_and_loss.compute_profit_and_loss_combo(self.currencies_calculations['combo_curr'])

        assert p_and_l_combo.item() == -1

    def test_compute_profit_and_loss_total(self):
        p_and_l_total = self.obj_compute_profit_and_loss.compute_profit_and_loss_total(self.currencies_calculations['return_excl_curr'])

        assert np.allclose(np.array(p_and_l_total.item()), np.array(6.82727431390140000)) == True









# @pytest.mark.parametrize("profit_and_loss_overview_origin, profit_and_loss_overview_results",
#                          [("profit_and_loss_overview_one_origin.csv", "profit_and_loss_overview_one_results.csv"),
#                           ("profit_and_loss_overview_two_origin.csv", "profit_and_loss_overview_two_results.csv")])
# def test_compute_profit_and_loss_combo(profit_and_loss_overview_origin, profit_and_loss_overview_results):
#     path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
#                                                profit_and_loss_overview_origin))
#     path_results = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
#                                                 profit_and_loss_overview_results))
#
#     profit_and_loss_results = pd.read_csv(path_results, sep=',', engine='python')
#     profit_and_loss_origin = pd.read_csv(path_origin, sep=',', engine='python')
#
#     assert np.allclose(np.array(profit_and_loss_results.Last_week.tolist()),
#                        np.array(profit_and_loss_origin.Last_week.tolist())) is True
#
#
# @pytest.mark.parametrize("profit_and_loss_overview_origin, profit_and_loss_overview_results",
#                          [("profit_and_loss_overview_one_origin.csv", "profit_and_loss_overview_one_results.csv"),
#                           ("profit_and_loss_overview_two_origin.csv", "profit_and_loss_overview_two_results.csv")])
# def test_compute_profit_and_loss_returns(profit_and_loss_overview_origin, profit_and_loss_overview_results):
#     path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
#                                                profit_and_loss_overview_origin))
#     path_results = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
#                                                 profit_and_loss_overview_results))
#
#     profit_and_loss_results = pd.read_csv(path_results, sep=',', engine='python')
#     profit_and_loss_origin = pd.read_csv(path_origin, sep=',', engine='python')
#
#     assert np.allclose(np.array(profit_and_loss_results.Total.tolist()),
#                        np.array(profit_and_loss_origin.Total.tolist())) is True
#
#
# @pytest.mark.parametrize("profit_and_loss_overview_origin, profit_and_loss_overview_results",
#                          [("profit_and_loss_overview_one_origin.csv", "profit_and_loss_overview_one_results.csv"),
#                           ("profit_and_loss_overview_two_origin.csv", "profit_and_loss_overview_two_results.csv")])
# def test_compute_profit_and_loss_spot(profit_and_loss_overview_origin, profit_and_loss_overview_results):
#     path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
#                                                profit_and_loss_overview_origin))
#     path_results = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
#                                                 profit_and_loss_overview_results))
#
#     profit_and_loss_results = pd.read_csv(path_results, sep=',', engine='python')
#     profit_and_loss_origin = pd.read_csv(path_origin, sep=',', engine='python')
#
#     assert np.allclose(np.array(profit_and_loss_results.Spot.tolist()),
#                        np.array(profit_and_loss_origin.Spot.tolist())) is True
#
#
# @pytest.mark.parametrize("profit_and_loss_overview_origin, profit_and_loss_overview_results",
#                          [("profit_and_loss_overview_one_origin.csv", "profit_and_loss_overview_one_results.csv"),
#                           ("profit_and_loss_overview_two_origin.csv", "profit_and_loss_overview_two_results.csv")])
# def test_compute_profit_and_loss_carry(profit_and_loss_overview_origin, profit_and_loss_overview_results):
#     path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
#                                                profit_and_loss_overview_origin))
#     path_results = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
#                                                 profit_and_loss_overview_results))
#
#     profit_and_loss_results = pd.read_csv(path_results, sep=',', engine='python')
#     profit_and_loss_origin = pd.read_csv(path_origin, sep=',', engine='python')
#
#     assert np.allclose(np.array(profit_and_loss_results.Carry.tolist()),
#                        np.array(profit_and_loss_origin.Carry.tolist())) is True
#
#
# @pytest.mark.parametrize("profit_and_loss_overview_origin, profit_and_loss_overview_results",
#                          [("profit_and_loss_notional_one_origin.csv", "profit_and_loss_notional_one_results.csv"),
#                           ("profit_and_loss_notional_two_origin.csv", "profit_and_loss_notional_two_results.csv")])
# def test_compute_profit_and_loss_notional(profit_and_loss_overview_origin, profit_and_loss_overview_results):
#     path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
#                                                "outputs_origin", profit_and_loss_overview_origin))
#     path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
#                                                "outputs_to_test", profit_and_loss_overview_results))
#
#     notional_results = pd.read_csv(path_result, sep=',', engine='python')
#     notional_origin = pd.read_csv(path_origin, sep=',', engine='python')
#
#     assert np.allclose(np.array(notional_origin.values), np.array(notional_results.values)) is True
#
#
# @pytest.mark.parametrize("profit_and_loss_overview_origin, profit_and_loss_overview_results",
#                          [("profit_and_loss_matr_one_origin.csv", "profit_and_loss_matr_one_results.csv"),
#                           ("profit_and_loss_matr_two_origin.csv", "profit_and_loss_matr_two_results.csv")])
# def test_compute_profit_and_loss_implemented_in_matr(profit_and_loss_overview_origin, profit_and_loss_overview_results):
#     path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
#                                                "outputs_origin", profit_and_loss_overview_origin))
#     path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources","effect",
#                                                "outputs_to_test", profit_and_loss_overview_results))
#
#     matr_results = pd.read_csv(path_result, sep=',', engine='python')
#     matr_origin = pd.read_csv(path_origin, sep=',', engine='python')
#
#     assert np.allclose(np.array(matr_origin.values), np.array(matr_results.values)) is True

