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


def test_compute_aggregate_total_incl_signals():
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "aggregate_total_incl_signals_origin.csv"))
    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test", "aggregate_total_incl_signals_results.csv"))

    agg_results = pd.read_csv(path_result, sep=',', engine='python')
    agg_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(agg_origin.Total_Incl_Signals.tolist()), np.array(agg_results.Total_Incl_Signals.tolist())) is True


def test_compute_aggregate_total_excl_signals():
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "aggregate_total_excl_signals_origin.csv"))
    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test", "aggregate_total_excl_signals_results.csv"))

    agg_results = pd.read_csv(path_result, sep=',', engine='python')
    agg_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(agg_origin.Total_Excl_Signals.tolist()), np.array(agg_results.Total_Excl_Signals.tolist())) is True


def test_compute_aggregate_spot_incl_signals():
    pass

def test_compute_aggregate_spot_excl_signals():
    pass

def test_compute_log_returns_excl_costs(currencies):
    pass

def test_compute_weighted_performance():
    pass







