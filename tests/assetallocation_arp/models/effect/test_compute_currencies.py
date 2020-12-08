import os
from unittest import TestCase
import pandas as pd

from assetallocation_arp.models.effect.compute_currencies import ComputeCurrencies
from data_etl.inputs_effect.compute_inflation_differential import ComputeInflationDifferential
from assetallocation_arp.common_libraries.dal_enums.strategy import Frequency, DayOfWeek, TrendIndicator, CarryType


class TestComputeCurrencies(TestCase):

    def setUp(self):
        all_data = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "all_date.csv")), sep=',', engine='python')
        all_data = all_data.set_index(pd.to_datetime(all_data.Date, format='%Y-%m-%d'))
        del all_data['Date']
        self.obj_import_data = ComputeCurrencies(asset_inputs=pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "asset_inputs.csv")), sep=',', engine='python'),
                                                 bid_ask_spread=10,
                                                 frequency_mat=Frequency.weekly,
                                                 end_date_mat=pd.to_datetime('23-09-2020', format='%d-%m-%Y'),
                                                 signal_day_mat=DayOfWeek.WED,
                                                 all_data=all_data)
        self.obj_import_data.process_all_data_effect()
        self.obj_import_data.start_date_calculations = pd.to_datetime('12-01-2000', format='%d-%m-%Y')
        self.obj_import_data.process_usd_eur_data_effect()

        # Inflation differential calculations
        obj_inflation_differential = ComputeInflationDifferential(dates_index=self.obj_import_data.dates_index)
        realtime_inflation_forecast, imf_data_update = True, False
        inflation_differential, currency_logs = obj_inflation_differential.compute_inflation_differential(
                                                realtime_inflation_forecast,
                                                self.obj_import_data.all_currencies_spot,
                                                self.obj_import_data.currencies_spot['currencies_spot_usd'],
                                                imf_data_update=imf_data_update)

        # Inputs
        self.trend_inputs = {'short_term': 4, 'long_term': 16, 'trend': TrendIndicator['total return']}
        self.carry_inputs = {'type': CarryType.real, 'inflation': inflation_differential}
        self.combo_inputs = {'cut_off': 2, 'incl_shorts': True, 'cut_off_s': 0.00, 'threshold': 0.25}

    def test_compute_trend(self):
        trend = self.obj_import_data.compute_trend(self.trend_inputs['trend'], self.trend_inputs['short_term'], self.trend_inputs['long_term'])

        path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "trend_brl_origin.csv"))
        trend_origin = pd.read_csv(path_origin, sep=',', engine='python')

        pd.testing.assert_series_equal(trend_origin.trend_BRL.reset_index(drop=True), trend[trend.columns.item()].reset_index(drop=True), check_names=False)

    def test_compute_carry(self):
        carry = self.obj_import_data.compute_carry(self.carry_inputs['type'], self.carry_inputs['inflation'])

        path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "carry_brl_origin.csv"))
        carry_origin = pd.read_csv(path_origin, sep=',', engine='python')

        pd.testing.assert_series_equal(carry_origin.carry_BRL.reset_index(drop=True), carry[carry.columns.item()].reset_index(drop=True), check_names=False)

    def test_compute_combo(self):
        # run trend and carry first
        self.obj_import_data.compute_trend(self.trend_inputs['trend'], self.trend_inputs['short_term'], self.trend_inputs['long_term'])
        self.obj_import_data.compute_carry(self.carry_inputs['type'], self.carry_inputs['inflation'])

        combo = self.obj_import_data.compute_combo(self.combo_inputs['cut_off'], self.combo_inputs['incl_shorts'], self.combo_inputs['cut_off_s'], self.combo_inputs['threshold'])

        path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "combo_brl_origin.csv"))
        combo_origin = pd.read_csv(path_origin, sep=',', engine='python')

        pd.testing.assert_series_equal(combo_origin.combo_BRL.reset_index(drop=True), combo[combo.columns.item()].reset_index(drop=True), check_names=False)

    def test_compute_return_ex_costs(self):
        # run combo first
        self.obj_import_data.compute_trend(self.trend_inputs['trend'], self.trend_inputs['short_term'], self.trend_inputs['long_term'])
        self.obj_import_data.compute_carry(self.carry_inputs['type'], self.carry_inputs['inflation'])
        self.obj_import_data.compute_combo(self.combo_inputs['cut_off'], self.combo_inputs['incl_shorts'], self.combo_inputs['cut_off_s'], self.combo_inputs['threshold'])

        ret = self.obj_import_data.compute_return_ex_costs()

        path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "return_ex_costs_brl_origin.csv"))
        ret_origin = pd.read_csv(path_origin, sep=',', engine='python')

        pd.testing.assert_series_equal(ret_origin.brl_return_ex_costs.reset_index(drop=True), ret[ret.columns.item()].reset_index(drop=True), check_names=False)

    def test_compute_return_incl_costs(self):
        # run combo and return_ex_costs first
        self.obj_import_data.compute_carry(self.carry_inputs['type'], self.carry_inputs['inflation'])
        self.obj_import_data.compute_trend(self.trend_inputs['trend'], self.trend_inputs['short_term'], self.trend_inputs['long_term'])
        self.obj_import_data.compute_combo(self.combo_inputs['cut_off'], self.combo_inputs['incl_shorts'], self.combo_inputs['cut_off_s'], self.combo_inputs['threshold'])
        self.obj_import_data.compute_return_ex_costs()

        ret = self.obj_import_data.compute_return_incl_costs()

        path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "return_incl_costs_brl_origin.csv"))
        ret_origin = pd.read_csv(path_origin, sep=',', engine='python')

        pd.testing.assert_series_equal(ret_origin.brl_return_incl_costs.reset_index(drop=True), ret[ret.columns.item()].reset_index(drop=True), check_names=False)

    def test_compute_spot_ex_costs(self):
        # run combo first
        self.obj_import_data.compute_carry(self.carry_inputs['type'], self.carry_inputs['inflation'])
        self.obj_import_data.compute_trend(self.trend_inputs['trend'], self.trend_inputs['short_term'], self.trend_inputs['long_term'])
        self.obj_import_data.compute_combo(self.combo_inputs['cut_off'], self.combo_inputs['incl_shorts'], self.combo_inputs['cut_off_s'], self.combo_inputs['threshold'])

        spot = self.obj_import_data.compute_spot_ex_costs()

        path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "spot_ex_costs_brl_origin.csv"))
        spot_origin = pd.read_csv(path_origin, sep=',', engine='python')

        pd.testing.assert_series_equal(spot_origin.brl_spot_ex_costs.reset_index(drop=True), spot[spot.columns.item()].reset_index(drop=True), check_names=False)

    def test_compute_spot_incl_costs(self):
        # run combo first
        self.obj_import_data.compute_carry(self.carry_inputs['type'], self.carry_inputs['inflation'])
        self.obj_import_data.compute_trend(self.trend_inputs['trend'], self.trend_inputs['short_term'], self.trend_inputs['long_term'])
        self.obj_import_data.compute_combo(self.combo_inputs['cut_off'], self.combo_inputs['incl_shorts'], self.combo_inputs['cut_off_s'], self.combo_inputs['threshold'])
        self.obj_import_data.compute_spot_ex_costs()

        spot = self.obj_import_data.compute_spot_incl_costs()

        path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "spot_incl_costs_brl_origin.csv"))
        spot_origin = pd.read_csv(path_origin, sep=',', engine='python')

        pd.testing.assert_series_equal(spot_origin.brl_spot_incl_costs.reset_index(drop=True), spot[spot.columns.item()].reset_index(drop=True), check_names=False)
