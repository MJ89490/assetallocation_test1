import os
import pytest
import numpy as np
import pandas as pd

"""
Notes: 
one: total return; 4 ;16; Yes; 2.0; 0.0; real; yes; 0.25; 1/N; 52; 10; 4
two: spot; 4 ;16; No; 2.0; 0.0; real; yes; 0.25 ;1/N ;52 ;10 ;4
"""


@pytest.mark.parametrize("risk_returns_table_origin, risk_returns_table_results",
                         [("risk_returns_table_one_origin.csv", "risk_returns_table_one_results.csv"),
                          ("risk_returns_table_two_origin.csv", "risk_returns_table_two_results.csv")])
def test_compute_excess_returns(risk_returns_table_origin, risk_returns_table_results):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                                               "risk_returns_table_one_origin.csv"))
    path_results = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                                                "risk_returns_table_one_results.csv"))
    risk_returns_results = pd.read_csv(path_results, sep=',', engine='python')
    risk_returns_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(risk_returns_results.excess_returns_with_signals.values),
                       np.array(risk_returns_origin.excess_returns_with_signals.values)) is True

    assert np.allclose(np.array(risk_returns_results.excess_returns_no_signals.values),
                       np.array(risk_returns_origin.excess_returns_no_signals.values)) is True


@pytest.mark.parametrize("risk_returns_table_origin, risk_returns_table_results",
                         [("risk_returns_table_one_origin.csv", "risk_returns_table_one_results.csv"),
                          ("risk_returns_table_two_origin.csv", "risk_returns_table_two_results.csv")])
def test_compute_std_dev(risk_returns_table_origin, risk_returns_table_results):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                                               "risk_returns_table_one_origin.csv"))
    path_results = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                                                "risk_returns_table_one_results.csv"))
    risk_returns_results = pd.read_csv(path_results, sep=',', engine='python')
    risk_returns_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(risk_returns_results.std_dev_with_signals.values),
                       np.array(risk_returns_origin.std_dev_with_signals.values)) is True

    assert np.allclose(np.array(risk_returns_results.std_dev_no_signals.values),
                       np.array(risk_returns_origin.std_dev_no_signals.values)) is True


@pytest.mark.parametrize("risk_returns_table_origin, risk_returns_table_results",
                         [("risk_returns_table_one_origin.csv", "risk_returns_table_one_results.csv"),
                          ("risk_returns_table_two_origin.csv", "risk_returns_table_two_results.csv")])
def test_compute_sharpe_ratio(risk_returns_table_origin, risk_returns_table_results):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                                               "risk_returns_table_one_origin.csv"))
    path_results = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                                                "risk_returns_table_one_results.csv"))

    risk_returns_results = pd.read_csv(path_results, sep=',', engine='python')
    risk_returns_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(risk_returns_results.sharpe_with_signals.values),
                       np.array(risk_returns_origin.sharpe_with_signals.values)) is True

    assert np.allclose(np.array(risk_returns_results.sharpe_no_signals.values),
                       np.array(risk_returns_origin.sharpe_no_signals.values)) is True


@pytest.mark.parametrize("risk_returns_table_origin, risk_returns_table_results",
                         [("risk_returns_table_one_origin.csv", "risk_returns_table_one_results.csv"),
                          ("risk_returns_table_two_origin.csv", "risk_returns_table_two_results.csv")])
def test_compute_max_drawdown(risk_returns_table_origin, risk_returns_table_results):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                                               "risk_returns_table_one_origin.csv"))
    path_results = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                                                "risk_returns_table_one_results.csv"))

    risk_returns_results = pd.read_csv(path_results, sep=',', engine='python')
    risk_returns_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(risk_returns_results.max_drawdown_with_signals.values),
                       np.array(risk_returns_origin.max_drawdown_with_signals.values)) is True

    assert np.allclose(np.array(risk_returns_results.max_drawdown_no_signals.values),
                       np.array(risk_returns_origin.max_drawdown_no_signals.values)) is True


@pytest.mark.parametrize("risk_returns_table_origin, risk_returns_table_results",
                         [("risk_returns_table_one_origin.csv", "risk_returns_table_one_results.csv"),
                          ("risk_returns_table_two_origin.csv", "risk_returns_table_two_results.csv")])
def test_compute_calmar_ratio(risk_returns_table_origin, risk_returns_table_results):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                                               "risk_returns_table_one_origin.csv"))
    path_results = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                                                "risk_returns_table_one_results.csv"))

    risk_returns_results = pd.read_csv(path_results, sep=',', engine='python')
    risk_returns_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(risk_returns_results.calmar_ratio_with_signals.values),
                       np.array(risk_returns_origin.calmar_ratio_with_signals.values)) is True

    assert np.allclose(np.array(risk_returns_results.calmar_ratio_no_signals.values),
                       np.array(risk_returns_origin.calmar_ratio_no_signals.values)) is True
