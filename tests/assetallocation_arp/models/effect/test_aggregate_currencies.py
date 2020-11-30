import os
import pandas as pd
from unittest import TestCase

from assetallocation_arp.models.effect.compute_aggregate_currencies import ComputeAggregateCurrencies
from assetallocation_arp.models.effect.compute_currencies import ComputeCurrencies
from data_etl.inputs_effect.compute_inflation_differential import ComputeInflationDifferential

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


class TestComputeAggregateCurrencies(TestCase):

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
        self.process_usd_eur_data_effect = self.obj_import_data.process_usd_eur_data_effect()

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
        self.obj_compute_agg_currencies = ComputeAggregateCurrencies(window=52,
                                                                     weight='1/N',
                                                                     dates_index=self.obj_import_data.dates_index,
                                                                     start_date_calculations=self.obj_import_data.start_date_calculations,
                                                                     prev_start_date_calc=self.obj_import_data.previous_start_date_calc)

    def test_compute_inverse_volatility(self):

        inv_volatility = self.obj_compute_agg_currencies.compute_inverse_volatility(self.process_usd_eur_data_effect['common_spot'])

        path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "inverse_volatility_brl_origin.csv"))
        inv_vol_origin = pd.read_csv(path_origin, sep=',', engine='python')

        pd.testing.assert_series_equal(inv_vol_origin.brl_inv_volatility.reset_index(drop=True), inv_volatility[inv_volatility.columns.item()].reset_index(drop=True), check_names=False)

    def test_compute_excl_signals_total_return(self):

        ret = self.obj_compute_agg_currencies.compute_excl_signals_total_return(self.process_usd_eur_data_effect['common_carry'])

        path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "excl_signals_total_return_brl_origin.csv"))
        ret_origin = pd.read_csv(path_origin, sep=',', engine='python')

        pd.testing.assert_series_equal(ret_origin.brl_excl_signals_total_return.reset_index(drop=True), ret[ret.columns.item()].reset_index(drop=True), check_names=False)

    def test_compute_excl_signals_spot_return(self):

        spot = self.obj_compute_agg_currencies.compute_excl_signals_spot_return(self.process_usd_eur_data_effect['common_spot'])

        path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "excl_signals_spot_return_brl_origin.csv"))
        spot_origin = pd.read_csv(path_origin, sep=',', engine='python')

        pd.testing.assert_series_equal(spot_origin.brl_excl_signals_spot_return.reset_index(drop=True), spot[spot.columns.item()].reset_index(drop=True), check_names=False)

    def test_compute_aggregate_total_incl_signals(self):

        ret = self.obj_compute_agg_currencies.compute_aggregate_total_incl_signals(self.currencies_calculations['return_incl_curr'], inverse_volatility=None)

        path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "aggregate_total_incl_signals_brl_origin.csv"))
        ret_origin = pd.read_csv(path_origin, sep=',', engine='python')

        pd.testing.assert_series_equal(ret_origin.brl_incl_signals.reset_index(drop=True), ret[ret.columns.item()].reset_index(drop=True), check_names=False)

    def test_compute_aggregate_total_excl_signals(self):
        ret_excl_costs = self.obj_compute_agg_currencies.compute_excl_signals_total_return(self.process_usd_eur_data_effect['common_carry'])
        ret = self.obj_compute_agg_currencies.compute_aggregate_total_excl_signals(ret_excl_costs, inverse_volatility=None)

        path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "aggregate_total_excl_signals_brl_origin.csv"))
        ret_origin = pd.read_csv(path_origin, sep=',', engine='python')

        pd.testing.assert_series_equal(ret_origin.brl_ex_signals.reset_index(drop=True), ret[ret.columns.item()].reset_index(drop=True), check_names=False)

    def test_compute_aggregate_spot_incl_signals(self):
        spot_incl_costs = self.currencies_calculations['spot_incl_curr']
        spot = self.obj_compute_agg_currencies.compute_aggregate_spot_incl_signals(spot_incl_costs, inverse_volatility=None)

        path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "aggregate_spot_incl_signals_brl_origin.csv"))
        spot_origin = pd.read_csv(path_origin, sep=',', engine='python')

        pd.testing.assert_series_equal(spot_origin.brl_spot_incl_signals.reset_index(drop=True), spot[spot.columns.item()].reset_index(drop=True), check_names=False)

    def test_compute_aggregate_spot_excl_signals(self):
        excl_signals_spot_ret = self.obj_compute_agg_currencies.compute_excl_signals_spot_return(spot_origin=self.process_usd_eur_data_effect['common_spot'])
        spot = self.obj_compute_agg_currencies.compute_aggregate_spot_excl_signals(excl_signals_spot_ret, inverse_volatility=None)

        path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "aggregate_spot_excl_signals_brl_origin.csv"))
        spot_origin = pd.read_csv(path_origin, sep=',', engine='python')

        pd.testing.assert_series_equal(spot_origin.brl_spot_excl_signals.reset_index(drop=True), spot[spot.columns.item()].reset_index(drop=True), check_names=False)

    def test_compute_log_returns_excl_costs(self):
        ret = self.obj_compute_agg_currencies.compute_excl_signals_total_return(self.process_usd_eur_data_effect['common_carry'])

        path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "log_returns_excl_costs_brl_origin.csv"))
        log_ret_origin = pd.read_csv(path_origin, sep=',', engine='python')

        log_ret = self.obj_compute_agg_currencies.compute_log_returns_excl_costs(ret)

        pd.testing.assert_series_equal(log_ret_origin.brl_log_returns.reset_index(drop=True), log_ret.iloc[:-1][log_ret.columns.item()].reset_index(drop=True), check_names=False)

    def test_compute_weighted_performance(self):
        ret = self.obj_compute_agg_currencies.compute_excl_signals_total_return(self.process_usd_eur_data_effect['common_carry'])
        log_ret = self.obj_compute_agg_currencies.compute_log_returns_excl_costs(ret)
        weighted_perf = self.obj_compute_agg_currencies.compute_weighted_performance(log_ret, self.currencies_calculations['combo_curr'], 0.03)

        path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "weighted_performance_brl_origin.csv"))
        weighted_perf_origin = pd.read_csv(path_origin, sep=',', engine='python')

        pd.testing.assert_series_equal(weighted_perf_origin.brl_weighted_perf.reset_index(drop=True), weighted_perf.iloc[:-1][weighted_perf.columns.item()].reset_index(drop=True), check_names=False)
