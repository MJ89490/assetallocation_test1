import os
import pandas as pd
import numpy as np
import pytest

"""
Notes: 
one: total return; 4 ;16; Yes; 2.0; 0.0; real; yes; 0.25; 1/N; 52; 10; 4
two: spot; 4 ;16; No; 2.0; 0.0; real; yes; 0.25 ;1/N ;52 ;10 ;4

"""


@pytest.fixture
def currencies():
    return ['BRL', 'TRY', 'THB']


@pytest.mark.parametrize("carry_origin, carry_results",
                         [("carry_one_origin.csv", "carry_one_results.csv"),
                          ("carry_two_origin.csv", "carry_two_results.csv")])
def test_compute_carry(currencies, carry_origin, carry_results):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                                               carry_origin))
    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                                               carry_results))

    carry_results = pd.read_csv(path_result, sep=',', engine='python')
    carry_origin = pd.read_csv(path_origin, sep=',', engine='python')

    for currency in currencies:
        assert np.allclose(np.array(carry_results[currency].tolist()), np.array(carry_origin[currency].tolist())) is True


@pytest.mark.parametrize("trend_origin, trend_results",
                         [("trend_one_origin.csv", "trend_one_results.csv"),
                          ("trend_two_origin.csv", "trend_two_results.csv")])
def test_compute_trend(currencies, trend_origin, trend_results):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                                               trend_origin))

    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                                               trend_results))

    trend_origin = pd.read_csv(path_origin, sep=',', engine='python')
    trend_results = pd.read_csv(path_result, sep=',', engine='python')

    for currency in currencies:
        assert np.allclose(np.array(trend_results[currency].tolist()), np.array(trend_origin[currency].tolist())) is True


@pytest.mark.parametrize("combo_origin, combo_results",
                         [("combo_one_origin.csv", "combo_one_results.csv"),
                          ("combo_two_origin.csv", "combo_two_results.csv")])
def test_compute_combo(currencies, combo_origin, combo_results):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                                               combo_origin))

    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                                               combo_results))

    combo_origin = pd.read_csv(path_origin, sep=',', engine='python')
    combo_results = pd.read_csv(path_result, sep=',', engine='python')

    for currency in currencies:
        assert np.allclose(np.array(combo_results[currency].tolist()), np.array(combo_origin[currency].tolist())) is True


@pytest.mark.parametrize("returns_ex_origin, returns_ex_results",
                         [("returns_ex_costs_one_origin.csv", "returns_ex_costs_one_results.csv"),
                          ("returns_ex_costs_two_origin.csv", "returns_ex_costs_two_results.csv")])
def test_compute_returns_ex_costs(currencies, returns_ex_origin, returns_ex_results):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                                               returns_ex_origin))

    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                                               returns_ex_results))

    returns_origin = pd.read_csv(path_origin, sep=',', engine='python')
    returns_results = pd.read_csv(path_result, sep=',', engine='python')

    for currency in currencies:
        assert np.allclose(np.array(returns_results[currency].tolist()), np.array(returns_origin[currency].tolist())) is True


@pytest.mark.parametrize("returns_incl_origin, returns_incl_results",
                         [("returns_incl_costs_one_origin.csv", "returns_incl_costs_one_results.csv"),
                          ("returns_incl_costs_two_origin.csv", "return_incl_costs_two_results.csv")])
def test_compute_return_incl_costs(currencies, returns_incl_origin, returns_incl_results):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                                               returns_incl_origin))

    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                                               returns_incl_results))

    returns_origin = pd.read_csv(path_origin, sep=',', engine='python')
    returns_results = pd.read_csv(path_result, sep=',', engine='python')

    for currency in currencies:
        assert np.allclose(np.array(returns_results[currency].tolist()), np.array(returns_origin[currency].tolist())) is True


@pytest.mark.parametrize("spot_ex_origin, spot_ex_results",
                         [("spot_ex_costs_one_origin.csv.", "spot_ex_costs_one_results.csv"),
                          ("spot_ex_costs_two_origin.csv.", "spot_ex_costs_two_results.csv")])
def test_compute_spot_ex_costs(currencies, spot_ex_origin, spot_ex_results):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                                               spot_ex_origin))

    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                                               spot_ex_results))

    spot_origin = pd.read_csv(path_origin, sep=',', engine='python')
    spot_results = pd.read_csv(path_result, sep=',', engine='python')

    for currency in currencies:

        assert np.allclose(np.array(spot_results[currency].tolist()), np.array(spot_origin[currency].tolist())) is True


@pytest.mark.parametrize("spot_incl_origin, spot_incl_results",
                         [("spot_incl_costs_one_origin.csv.", "spot_incl_costs_one_results.csv"),
                          ("spot_incl_costs_two_origin.csv.", "spot_incl_costs_two_results.csv")])
def test_compute_spot_incl_costs(currencies, spot_incl_origin, spot_incl_results):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                                               spot_incl_origin))

    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                                               spot_incl_results))

    spot_origin = pd.read_csv(path_origin, sep=',', engine='python')
    spot_results = pd.read_csv(path_result, sep=',', engine='python')

    for currency in currencies:
        assert np.allclose(np.array(spot_results[currency].tolist()), np.array(spot_origin[currency].tolist())) is True