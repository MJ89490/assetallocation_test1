import os
from unittest import TestCase
import pandas as pd

from assetallocation_arp.models.effect.compute_currencies import ComputeCurrencies
from data_etl.inputs_effect.compute_inflation_differential import ComputeInflationDifferential
from assetallocation_arp.common_libraries.dal_enums.strategy import Frequency, DayOfWeek, TrendIndicator, CarryType


class TestComputeInflationDifferential(TestCase):

    def setUp(self):
        all_data = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "all_date.csv")), sep=',', engine='python')

        all_data = all_data.set_index(pd.to_datetime(all_data.Date, format='%Y-%m-%d'))
        del all_data['Date']

        self.obj_import_data = ComputeCurrencies(asset_inputs=pd.read_csv(os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "asset_inputs.csv")),
            sep=',', engine='python'), bid_ask_spread=10, frequency_mat=Frequency.weekly,
            end_date_mat=pd.to_datetime('23-09-2020', format='%d-%m-%Y'), signal_day_mat=DayOfWeek.WED,
            all_data=all_data)

        self.obj_import_data.process_all_data_effect()
        self.obj_import_data.start_date_calculations = pd.to_datetime('12-01-2000', format='%d-%m-%Y')
        self.obj_import_data.process_usd_eur_data_effect()

        self.obj_inflation_differential = ComputeInflationDifferential(dates_index=self.obj_import_data.dates_index)

        # Inputs
        self.realtime_inf_forecast, self.imf_data_update = True, False

    def test_compute_inflation_release(self):
        inf_release, years_zero_inf, months_inf = self.obj_inflation_differential.compute_inflation_release(self.realtime_inf_forecast)

        inf_results = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "inflation_release_brl_origin.csv")), sep=',', engine='python')
        year_results = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "years_zero_inflation_brl_origin.csv")), sep=',', engine='python')
        month_results = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "months_inflation_brl_origin.csv")), sep=',', engine='python')

        pd.testing.assert_series_equal(inf_release.Inflation_Release.reset_index(drop=True), inf_results.brl_inflation_release.reset_index(drop=True), check_names=False)
        pd.testing.assert_series_equal(years_zero_inf.Years.reset_index(drop=True), year_results.brl_years.reset_index(drop=True), check_names=False)
        pd.testing.assert_series_equal(months_inf.Months.reset_index(drop=True), month_results.brl_months.reset_index(drop=True), check_names=False)

    def test_compute_inflation_differential(self):
        inf_diff_origin = self.obj_inflation_differential.compute_inflation_differential(self.realtime_inf_forecast,
                                                                                         self.obj_import_data.all_currencies_spot,
                                                                                         self.obj_import_data.currencies_spot['currencies_spot_usd'],
                                                                                         self.imf_data_update)

        inf_results = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "inflation_differential_brl_origin.csv")), sep=',', engine='python')

        pd.testing.assert_series_equal(inf_diff_origin[0][inf_diff_origin[0].columns.item()].reset_index(drop=True), inf_results.brl_inflation_diff.reset_index(drop=True), check_names=False)
