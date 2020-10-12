import os
import pandas as pd

from assetallocation_arp.models.effect.compute_currencies import ComputeCurrencies
from data_etl.inputs_effect.compute_inflation_differential import ComputeInflationDifferential

path_all_data = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "all_date.csv"))
path_asset = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "asset_inputs.csv"))

all_data = pd.read_csv(path_all_data, sep=',', engine='python')
asset_inputs = pd.read_csv(path_asset, sep=',', engine='python')

all_data = all_data.set_index(pd.to_datetime(all_data.Date, format='%Y-%m-%d'))
del all_data['Date']

obj_import_data = ComputeCurrencies(asset_inputs=asset_inputs,
                                    bid_ask_spread=10,
                                    frequency_mat='weekly',
                                    start_date_mat='06/01/1999',
                                    end_date_mat='23/09/2020',
                                    signal_day_mat='WED', all_data=all_data)
obj_import_data.process_data_effect()
obj_import_data.start_date_calculations = pd.to_datetime('12-01-2000', format='%d-%m-%Y')

obj_inflation_differential = ComputeInflationDifferential(dates_index=obj_import_data.dates_index)

realtime_inflation_forecast, imf_data_update = 'Yes', False


def test_compute_inflation_release():

    path_year = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "years_zero_inflation.csv"))
    path_month = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "months_inflation.csv"))
    path_inf = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "inflation_release.csv"))

    inf_results = pd.read_csv(path_inf, sep=',', engine='python')
    year_results = pd.read_csv(path_year, sep=',', engine='python')
    month_results = pd.read_csv(path_month, sep=',', engine='python')

    inf_diff_origin, year_origin, month_origin = obj_inflation_differential.compute_inflation_release(realtime_inflation_forecast)

    pd.testing.assert_series_equal(inf_diff_origin.Inflation_Release.reset_index(drop=True), inf_results.Inflation_Release.reset_index(drop=True))
    pd.testing.assert_series_equal(year_origin.Years.reset_index(drop=True), year_results.Years.reset_index(drop=True))
    pd.testing.assert_series_equal(month_origin.Months.reset_index(drop=True), month_results.Months.reset_index(drop=True))


def test_compute_inflation_differential():

    path_dates_inf_diff = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "inflation_differential.csv"))
    inf_diff_results = pd.read_csv(path_dates_inf_diff, sep=',', engine='python')

    inf_diff_origin = obj_inflation_differential.compute_inflation_differential(
                      realtime_inflation_forecast, obj_import_data.all_currencies_spot,
                      obj_import_data.currencies_spot['currencies_spot_usd'], imf_data_update)

    pd.testing.assert_series_equal(inf_diff_origin['Inflation_Differential_BRLUSD Curncy'].reset_index(drop=True),
                                   inf_diff_results.Inflation_Diff.reset_index(drop=True), check_names=False)
