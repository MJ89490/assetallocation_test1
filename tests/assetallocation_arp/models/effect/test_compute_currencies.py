import os
import pandas as pd
import numpy as np
import pytest


# TODO DO THE UNIT TESTS WHILE DOING THE FRONTEND

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
                                    end_date_mat='23/09/2020',
                                    signal_day_mat='WED', all_data=all_data)
spx_index_values = obj_import_data.process_data_effect()
obj_import_data.start_date_calculations = pd.to_datetime('12-01-2000', format='%d-%m-%Y')
obj_import_data.process_data_config_effect()

# -------------------------- Inflation differential calculations ------------------------------------------------- #
obj_inflation_differential = ComputeInflationDifferential(dates_index=obj_import_data.dates_index)
realtime_inflation_forecast, imf_data_update = 'Yes', False

inflation_differential = obj_inflation_differential.compute_inflation_differential(
                         realtime_inflation_forecast, obj_import_data.all_currencies_spot,
                         obj_import_data.currencies_spot['currencies_spot_usd'],
                         imf_data_update=imf_data_update)

# -------------------------- Carry - Trend - Combo - Returns - Spot ---------------------------------------------- #

carry_inputs = {'type': 'real', 'inflation': inflation_differential}
trend_inputs = {'short_term': 4, 'long_term': 16, 'trend': 'total return'}
combo_inputs = {'cut_off': 0.02 * 100, 'incl_shorts': 'Yes', 'cut_off_s': 0.00 * 100, 'threshold': 0.025 * 100}

currencies_calculations = obj_import_data.run_compute_currencies(carry_inputs, trend_inputs, combo_inputs)


# currencies_calculations = obj_import_data.run_compute_currencies(carry_inputs, trend_inputs, combo_inputs)

def test_compute_carry():
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "carry_brl_origin.csv"))
    carry_origin = pd.read_csv(path_origin, sep=',', engine='python')

    carry_inputs = {'type': 'real', 'inflation': inflation_differential}
    carry_results = obj_import_data.compute_carry(carry_inputs['type'], carry_inputs['inflation'])
    pd.testing.assert_series_equal(carry_origin.carry_BRL.reset_index(drop=True), carry_results['Carry_BRLUSD Curncy'].reset_index(drop=True), check_names=False)


def test_compute_combo():

    combo_inputs = {'cut_off': 0.02 * 100, 'incl_shorts': 'Yes', 'cut_off_s': 0.00 * 100, 'threshold': 0.025 * 100}
    r = obj_import_data.compute_combo(combo_inputs['cut_off'], combo_inputs['incl_shorts'], combo_inputs['cut_off_s'], combo_inputs['threshold'])


    print()
# @pytest.mark.parametrize("trend_origin, trend_results",
#                          [("trend_one_origin.csv", "trend_one_results.csv"),
#                           ("trend_two_origin.csv", "trend_two_results.csv")])
# def test_compute_trend(currencies, trend_origin, trend_results):
#     path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
#                                                trend_origin))
#
#     path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
#                                                trend_results))
#
#     trend_origin = pd.read_csv(path_origin, sep=',', engine='python')
#     trend_results = pd.read_csv(path_result, sep=',', engine='python')
#
#     for currency in currencies:
#         assert np.allclose(np.array(trend_results[currency].tolist()), np.array(trend_origin[currency].tolist())) is True
#
#
# @pytest.mark.parametrize("combo_origin, combo_results",
#                          [("combo_one_origin.csv", "combo_one_results.csv"),
#                           ("combo_two_origin.csv", "combo_two_results.csv")])
# def test_compute_combo(currencies, combo_origin, combo_results):
#     path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
#                                                combo_origin))
#
#     path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
#                                                combo_results))
#
#     combo_origin = pd.read_csv(path_origin, sep=',', engine='python')
#     combo_results = pd.read_csv(path_result, sep=',', engine='python')
#
#     for currency in currencies:
#         assert np.allclose(np.array(combo_results[currency].tolist()), np.array(combo_origin[currency].tolist())) is True
#
#
# @pytest.mark.parametrize("returns_ex_origin, returns_ex_results",
#                          [("returns_ex_costs_one_origin.csv", "returns_ex_costs_one_results.csv"),
#                           ("returns_ex_costs_two_origin.csv", "returns_ex_costs_two_results.csv")])
# def test_compute_returns_ex_costs(currencies, returns_ex_origin, returns_ex_results):
#     path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
#                                                returns_ex_origin))
#
#     path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
#                                                returns_ex_results))
#
#     returns_origin = pd.read_csv(path_origin, sep=',', engine='python')
#     returns_results = pd.read_csv(path_result, sep=',', engine='python')
#
#     for currency in currencies:
#         assert np.allclose(np.array(returns_results[currency].tolist()), np.array(returns_origin[currency].tolist())) is True
#
#
# @pytest.mark.parametrize("returns_incl_origin, returns_incl_results",
#                          [("returns_incl_costs_one_origin.csv", "returns_incl_costs_one_results.csv"),
#                           ("returns_incl_costs_two_origin.csv", "return_incl_costs_two_results.csv")])
# def test_compute_return_incl_costs(currencies, returns_incl_origin, returns_incl_results):
#     path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
#                                                returns_incl_origin))
#
#     path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
#                                                returns_incl_results))
#
#     returns_origin = pd.read_csv(path_origin, sep=',', engine='python')
#     returns_results = pd.read_csv(path_result, sep=',', engine='python')
#
#     for currency in currencies:
#         assert np.allclose(np.array(returns_results[currency].tolist()), np.array(returns_origin[currency].tolist())) is True
#
#
# @pytest.mark.parametrize("spot_ex_origin, spot_ex_results",
#                          [("spot_ex_costs_one_origin.csv.", "spot_ex_costs_one_results.csv"),
#                           ("spot_ex_costs_two_origin.csv.", "spot_ex_costs_two_results.csv")])
# def test_compute_spot_ex_costs(currencies, spot_ex_origin, spot_ex_results):
#     path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
#                                                spot_ex_origin))
#
#     path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
#                                                spot_ex_results))
#
#     spot_origin = pd.read_csv(path_origin, sep=',', engine='python')
#     spot_results = pd.read_csv(path_result, sep=',', engine='python')
#
#     for currency in currencies:
#
#         assert np.allclose(np.array(spot_results[currency].tolist()), np.array(spot_origin[currency].tolist())) is True
#
#
# @pytest.mark.parametrize("spot_incl_origin, spot_incl_results",
#                          [("spot_incl_costs_one_origin.csv.", "spot_incl_costs_one_results.csv"),
#                           ("spot_incl_costs_two_origin.csv.", "spot_incl_costs_two_results.csv")])
# def test_compute_spot_incl_costs(currencies, spot_incl_origin, spot_incl_results):
#     path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
#                                                spot_incl_origin))
#
#     path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
#                                                spot_incl_results))
#
#     spot_origin = pd.read_csv(path_origin, sep=',', engine='python')
#     spot_results = pd.read_csv(path_result, sep=',', engine='python')
#
#     for currency in currencies:
#         assert np.allclose(np.array(spot_results[currency].tolist()), np.array(spot_origin[currency].tolist())) is True