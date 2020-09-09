import os
import pytest
import pandas as pd
import numpy as np

"""
Notes: 
one: total return; 4 ;16; Yes; 2.0; 0.0; real; yes; 0.25; 1/N; 52; 10; 4

"""

@pytest.fixture
def currencies():
    return ['BRL', 'TRY', 'THB']


# def test_compute_inverse_volatility(currencies):
#     # TODO A MODIFIER
#     path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "inverse_volatilities_origin.csv"))
#     path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test", "inverse_volatilities_results.csv"))
#
#     volatility_results = pd.read_csv(path_result, sep=',', engine='python')
#     volatility_origin = pd.read_csv(path_origin, sep=',', engine='python')
#
#     for currency in currencies:
#         assert np.allclose(np.array(volatility_origin[currency].tolist()), np.array(volatility_results[currency].tolist())) is True

@pytest.mark.parametrize("excl_signals_total_return_origin, excl_signals_total_return_results",
                         [("excl_signals_total_return_one_origin.csv", "excl_signals_total_return_one_results.csv")])
def test_compute_excl_signals_total_return(currencies, excl_signals_total_return_origin, excl_signals_total_return_results):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                               "outputs_origin", excl_signals_total_return_origin))
    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                               "outputs_to_test", excl_signals_total_return_results))

    signals_results = pd.read_csv(path_result, sep=',', engine='python')
    signals_origin = pd.read_csv(path_origin, sep=',', engine='python')

    for currency in currencies:
        assert np.allclose(np.array(signals_origin[currency].tolist()), np.array(signals_results[currency].tolist())) is True


@pytest.mark.parametrize("excl_signals_spot_return_origin, excl_signals_spot_return_results",
                         [("excl_signals_spot_return_one_origin.csv", "excl_signals_spot_return_one_results.csv")])
def test_compute_excl_signals_spot_return(currencies, excl_signals_spot_return_origin, excl_signals_spot_return_results):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                               "outputs_origin", excl_signals_spot_return_origin))
    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                               "outputs_to_test", excl_signals_spot_return_results))

    signals_results = pd.read_csv(path_result, sep=',', engine='python')
    signals_origin = pd.read_csv(path_origin, sep=',', engine='python')

    for currency in currencies:
        assert np.allclose(np.array(signals_origin[currency].tolist()), np.array(signals_results[currency].tolist())) is True


@pytest.mark.parametrize("log_returns_excl_costs_origin, log_returns_excl_costs_results",
                         [("log_returns_excl_costs_one_origin.csv", "log_returns_excl_costs_one_results.csv")])
def test_compute_log_returns_excl_costs(currencies, log_returns_excl_costs_origin, log_returns_excl_costs_results):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                               "outputs_origin", log_returns_excl_costs_origin))
    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                               "outputs_to_test", log_returns_excl_costs_results))

    log_results = pd.read_csv(path_result, sep=',', engine='python')
    log_origin = pd.read_csv(path_origin, sep=',', engine='python')

    for currency in currencies:
        assert np.allclose(np.array(log_origin[currency].tolist()), np.array(log_results[currency].tolist())) is True


@pytest.mark.parametrize("weighted_performance_origin, weighted_performance_results",
                         [("weighted_performance_one_origin.csv", "weighted_performance_one_results.csv")])
def test_compute_weighted_performance(weighted_performance_origin, weighted_performance_results):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                               "outputs_origin", weighted_performance_origin))
    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                               "outputs_to_test", weighted_performance_results))

    weighted_results = pd.read_csv(path_result, sep=',', engine='python')
    weighted_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(weighted_origin.Weighted_Performance.tolist()),
                       np.array(weighted_results.Weighted_Performance.tolist())) is True


@pytest.mark.parametrize("agg_total_incl_signals_origin, agg_total_incl_signals_results, name_col",
                        [("aggregate_total_incl_signals_one_origin.csv",
                          "aggregate_total_incl_signals_one_results.csv", "Total_Incl_Signals")])
def test_compute_aggregate_total_incl_signals(agg_total_incl_signals_origin, agg_total_incl_signals_results, name_col):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                               "outputs_origin", agg_total_incl_signals_origin))
    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                               "outputs_to_test", agg_total_incl_signals_results))

    agg_results = pd.read_csv(path_result, sep=',', engine='python')
    agg_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(agg_origin[name_col].tolist()), np.array(agg_results[name_col].tolist())) is True


@pytest.mark.parametrize("agg_total_excl_signals_origin, agg_total_excl_signals_results, name_col",
                        [("aggregate_total_excl_signals_one_origin.csv",
                          "aggregate_total_excl_signals_one_results.csv", "Total_Excl_Signals")])
def test_compute_aggregate_total_excl_signals(agg_total_excl_signals_origin, agg_total_excl_signals_results, name_col):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                               "outputs_origin", agg_total_excl_signals_origin))
    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                               "outputs_to_test", agg_total_excl_signals_results))

    agg_results = pd.read_csv(path_result, sep=',', engine='python')
    agg_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(agg_origin[name_col].tolist()), np.array(agg_results[name_col].tolist())) is True


@pytest.mark.parametrize("agg_spot_incl_signals_origin, agg_spot_incl_signals_results, name_col",
                        [("aggregate_spot_incl_signals_one_origin.csv", "aggregate_spot_incl_signals_one_results.csv",
                          "Spot_Incl_Signals")])
def test_compute_aggregate_spot_incl_signals(agg_spot_incl_signals_origin, agg_spot_incl_signals_results, name_col):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                               "outputs_origin", agg_spot_incl_signals_origin))
    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                               "outputs_to_test", agg_spot_incl_signals_results ))

    agg_results = pd.read_csv(path_result, sep=',', engine='python')
    agg_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(agg_origin[name_col].tolist()), np.array(agg_results[name_col].tolist())) is True


@pytest.mark.parametrize("agg_spot_excl_signals_origin, agg_spot_excl_signals_results, name_col",
                        [("aggregate_spot_excl_signals_one_origin.csv",
                          "aggregate_spot_excl_signals_one_results.csv", "Spot_Excl_Signals")])
def test_compute_aggregate_spot_excl_signals(agg_spot_excl_signals_origin, agg_spot_excl_signals_results, name_col):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                               "outputs_origin", agg_spot_excl_signals_origin))
    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                               "outputs_to_test", agg_spot_excl_signals_results))

    agg_results = pd.read_csv(path_result, sep=',', engine='python')
    agg_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(agg_origin[name_col].tolist()), np.array(agg_results[name_col].tolist())) is True











