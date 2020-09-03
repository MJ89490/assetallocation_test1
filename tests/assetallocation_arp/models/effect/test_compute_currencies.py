import os
import pandas as pd
import numpy as np
import pytest


@pytest.fixture
def currencies():
    return ['HUF', 'PLN', 'PEN', 'BRL', 'ARS', 'MXN', 'COP', 'CLP', 'TRY', 'RUB', 'ZAR', 'CNY', 'KRW', 'IDR', 'INR', 'PHP',
            'THB', 'CZK']


@pytest.mark.parametrize("carry_origin, carry_results",
                         [("carry_nominal_origin.csv", "carry_nominal_results.csv"),
                          ("carry_origin.csv", "carry_results.csv")])
def test_compute_carry(currencies, carry_origin, carry_results):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                                               carry_origin))
    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                                               carry_results))

    carry_results = pd.read_csv(path_result, sep=',', engine='python')
    carry_origin = pd.read_csv(path_origin, sep=',', engine='python')

    for currency in currencies:
        assert np.allclose(np.array(carry_results[currency].tolist()), np.array(carry_origin[currency].tolist())) is True


def test_compute_trend(currencies):

    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                                               "trend_total_returns_origin.csv"))

    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                                               "trend_total_returns_results.csv"))

    trend_origin = pd.read_csv(path_origin, sep=',', engine='python')
    trend_results = pd.read_csv(path_result, sep=',', engine='python')

    for currency in currencies:
        assert np.allclose(np.array(trend_results[currency].tolist()), np.array(trend_origin[currency].tolist())) is True


def test_compute_combo(currencies):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                                               "combo_origin.csv"))

    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                                               "combo_results.csv"))

    combo_origin = pd.read_csv(path_origin, sep=',', engine='python')
    combo_results = pd.read_csv(path_result, sep=',', engine='python')

    for currency in currencies:
        assert np.allclose(np.array(combo_results[currency].tolist()), np.array(combo_origin[currency].tolist())) is True


def test_compute_returns_ex_costs(currencies):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                                               "returns_ex_costs_origin.csv"))

    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                                               "returns_ex_costs_results.csv"))

    returns_origin = pd.read_csv(path_origin, sep=',', engine='python')
    returns_results = pd.read_csv(path_result, sep=',', engine='python')

    for currency in currencies:
        assert np.allclose(np.array(returns_results[currency].tolist()), np.array(returns_origin[currency].tolist())) is True


def test_compute_return_incl_costs(currencies):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                                               "returns_incl_costs_origin.csv"))

    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                                               "returns_incl_costs_results.csv"))

    returns_origin = pd.read_csv(path_origin, sep=',', engine='python')
    returns_results = pd.read_csv(path_result, sep=',', engine='python')

    for currency in currencies:
        assert np.allclose(np.array(returns_results[currency].tolist()), np.array(returns_origin[currency].tolist())) is True


def test_compute_spot_ex_costs(currencies):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                                               "spot_ex_costs_origin.csv"))

    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                                               "spot_ex_costs_results.csv"))

    spot_origin = pd.read_csv(path_origin, sep=',', engine='python')
    spot_results = pd.read_csv(path_result, sep=',', engine='python')

    for currency in currencies:

        assert np.allclose(np.array(spot_results[currency].tolist()), np.array(spot_origin[currency].tolist())) is True


def test_compute_spot_incl_costs(currencies):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                                               "spot_incl_costs_origin.csv"))

    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                                               "spot_incl_costs_results.csv"))

    spot_origin = pd.read_csv(path_origin, sep=',', engine='python')
    spot_results = pd.read_csv(path_result, sep=',', engine='python')

    for currency in currencies:

        assert np.allclose(np.array(spot_results[currency].tolist()), np.array(spot_origin[currency].tolist())) is True