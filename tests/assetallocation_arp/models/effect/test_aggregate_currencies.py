import os
import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def currencies():
    return ['ARS', 'BRL', 'PEN', 'MXN', 'COP', 'CLP', 'TRY', 'RUB', 'CZK', 'HUF', 'PLN', 'ZAR', 'CNY', 'KRW', 'IDR',
            'PHP', 'THB', 'INR']


def test_compute_inverse_volatility(currencies):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "inverse_volatilities_origin.csv"))
    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test", "inverse_volatilities_results.csv"))

    volatility_results = pd.read_csv(path_result, sep=',', engine='python')
    volatility_origin = pd.read_csv(path_origin, sep=',', engine='python')

    for currency in currencies:
        assert np.allclose(np.array(volatility_origin[currency].tolist()), np.array(volatility_results[currency].tolist())) is True


def test_compute_excl_signals_total_return(currencies):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "excl_signals_total_returns_origin.csv"))
    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test", "excl_signals_total_return_results.csv"))

    signals_results = pd.read_csv(path_result, sep=',', engine='python')
    signals_origin = pd.read_csv(path_origin, sep=',', engine='python')

    for currency in currencies:
        assert np.allclose(np.array(signals_origin[currency].tolist()), np.array(signals_results[currency].tolist())) is True


def test_compute_excl_signals_spot_return(currencies):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "excl_signals_spot_return_origin.csv"))
    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test", "excl_signals_spot_return_results.csv"))

    signals_results = pd.read_csv(path_result, sep=',', engine='python')
    signals_origin = pd.read_csv(path_origin, sep=',', engine='python')

    for currency in currencies:
        assert np.allclose(np.array(signals_origin[currency].tolist()), np.array(signals_results[currency].tolist())) is True


@pytest.mark.parametrize("agg_spot_incl_signals_origin, agg_spot_incl_signals_results, name_column",
                        [("aggregate_total_incl_signals_origin.csv",
                          "aggregate_total_incl_signals_results.csv", "Total_Incl_Signals"),
                         ("aggregate_total_incl_signals_inv_vol_origin.csv",
                          "aggregate_total_incl_signals_inv_vol_results.csv", "Total_Incl_Signals_Inv_Vol")])
def test_compute_aggregate_total_incl_signals(agg_spot_incl_signals_origin, agg_spot_incl_signals_results, name_column):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", agg_spot_incl_signals_origin))
    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test", agg_spot_incl_signals_results))

    agg_results = pd.read_csv(path_result, sep=',', engine='python')
    agg_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(agg_origin[name_column].tolist()), np.array(agg_results[name_column].tolist())) is True


def test_compute_aggregate_total_excl_signals():
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "aggregate_total_excl_signals_origin.csv"))
    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test", "aggregate_total_excl_signals_results.csv"))

    agg_results = pd.read_csv(path_result, sep=',', engine='python')
    agg_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(agg_origin.Total_Excl_Signals.tolist()), np.array(agg_results.Total_Excl_Signals.tolist())) is True


# @pytest.mark.parametrize("aggregate_spot_incl_signals_origin, aggregate_spot_incl_signals_results, name_column",
#                         [("aggregate_spot_incl_signals_origin.csv", "aggregate_spot_incl_signals_results.csv"),
#                          ("aggregate_total_incl_signals_inv_vol_origin.csv", "aggregate_total_incl_signals_inv_vol_results.csv", "Total_Incl_Signals_Inv_Vol")])
# def test_compute_aggregate_spot_incl_signals(aggregate_spot_incl_signals_origin, aggregate_spot_incl_signals_results):
#     path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", aggregate_spot_incl_signals_origin))
#     path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test", aggregate_spot_incl_signals_results ))
#
#     agg_results = pd.read_csv(path_result, sep=',', engine='python')
#     agg_origin = pd.read_csv(path_origin, sep=',', engine='python')
#
#     assert np.allclose(np.array(agg_origin.values),
#                        np.array(agg_results.values)) is True


def test_compute_aggregate_spot_excl_signals():
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "aggregate_spot_excl_signals_origin.csv"))
    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test", "aggregate_spot_excl_signals_results.csv"))

    agg_results = pd.read_csv(path_result, sep=',', engine='python')
    agg_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(agg_origin.Spot_Excl_Signals.tolist()),
                       np.array(agg_results.Spot_Excl_Signals.tolist())) is True


def test_compute_log_returns_excl_costs(currencies):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "log_returns_excl_costs_origin.csv"))
    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test", "log_returns_excl_costs_results.csv"))

    log_results = pd.read_csv(path_result, sep=',', engine='python')
    log_origin = pd.read_csv(path_origin, sep=',', engine='python')

    for currency in currencies:
        assert np.allclose(np.array(log_origin[currency].tolist()),
                           np.array(log_results[currency].tolist())) is True

def test_compute_weighted_performance():
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "weighted_performance_origin.csv"))
    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test", "weighted_performance_results.csv"))

    weighted_results = pd.read_csv(path_result, sep=',', engine='python')
    weighted_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(weighted_origin.Weighted_Performance.tolist()),
                       np.array(weighted_results.Weighted_Performance.tolist())) is True







