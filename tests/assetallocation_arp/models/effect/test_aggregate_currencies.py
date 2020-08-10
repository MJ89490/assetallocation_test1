import os
import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def currencies():
    return ['BRL', 'PEN',	'ARS', 'MXN', 'COP', 'CLP', 'TRY', 'RUB', 'CZK', 'HUF', 'PLN', 'ZAR', 'CNY', 'KRW', 'IDR',
            'INR', 'PHP', 'THB']


def test_compute_inverse_volatility(currencies):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "inflation_differential_origin.csv"))
    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test", "inflation_differential_results.csv"))

    volatility_results = pd.read_csv(path_result, sep=',', engine='python')
    volatility_origin = pd.read_csv(path_origin, sep=',', engine='python')

    for currency in currencies:
        assert np.allclose(np.array(volatility_origin[currency].tolist()), np.array(volatility_results[currency].tolist())) is True


def test_compute_excl_signals_total_return(currencies):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "excl_signals_total_return_origin.csv"))
    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test", "excl_signals_total_return_results.csv"))

    signals_total_results = pd.read_csv(path_result, sep=',', engine='python')
    signals_total_origin = pd.read_csv(path_origin, sep=',', engine='python')

    for currency in currencies:
        assert np.allclose(np.array(signals_total_results[currency].tolist()), np.array(signals_total_origin[currency].tolist())) is True


def test_compute_excl_signals_spot_return(currencies):
    pass


def test_compute_log_returns_excl_costs(currencies):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "log_returns_excl_costs_origin.csv"))
    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test", "log_returns_excl_costs_results.csv"))

    log_returns_results = pd.read_csv(path_result, sep=',', engine='python')
    log_returns_origin = pd.read_csv(path_origin, sep=',', engine='python')

    for currency in currencies:
        assert np.allclose(np.array(log_returns_origin[currency].tolist()), np.array(log_returns_results[currency].tolist())) is True










