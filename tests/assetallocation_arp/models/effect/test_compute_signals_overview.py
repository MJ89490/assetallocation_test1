import os
import pytest
import numpy as np
import pandas as pd

"""
Notes: 
one: total return; 4 ;16; Yes; 2.0; 0.0; real; yes; 0.25; 1/N; 52; 10; 4
two: spot; 4 ;16; No; 2.0; 0.0; real; yes; 0.25 ;1/N ;52 ;10 ;4
"""


@pytest.mark.parametrize("signal_origin, signal_results",
                         [("signals_overview_one_origin.csv", "signals_overview_one_results.csv"),
                          ("signals_overview_two_origin.csv", "signals_overview_two_results.csv")])
def test_compute_signals_real_carry(signal_origin, signal_results):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                                               signal_origin))
    path_results = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                                                signal_results))

    signal_results = pd.read_csv(path_results, sep=',', engine='python')
    signal_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(signal_results.Real_carry.tolist()),
                       np.array(signal_origin.Real_carry.tolist())) is True


@pytest.mark.parametrize("signal_origin, signal_results",
                         [("signals_overview_one_origin.csv", "signals_overview_one_results.csv"),
                          ("signals_overview_two_origin.csv", "signals_overview_two_results.csv")])
def test_compute_signals_trend(signal_origin, signal_results):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                                               signal_origin))
    path_results = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                                                signal_results))

    signal_results = pd.read_csv(path_results, sep=',', engine='python')
    signal_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(signal_results.Trend.tolist()),
                       np.array(signal_origin.Trend.tolist())) is True


@pytest.mark.parametrize("signal_origin, signal_results",
                         [("signals_overview_one_origin.csv", "signals_overview_one_results.csv"),
                          ("signals_overview_two_origin.csv", "signals_overview_two_results.csv")])
def test_compute_signals_combo(signal_origin, signal_results):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                                               signal_origin))
    path_results = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                                                signal_results))

    signal_results = pd.read_csv(path_results, sep=',', engine='python')
    signal_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(signal_results.This_week.tolist()),
                       np.array(signal_origin.This_week.tolist())) is True


@pytest.mark.parametrize("drawdown_size_origin, drawdown_size_results",
                         [("drawdown_position_size_matr_one_origin.csv", "drawdown_position_size_matr_one_results.csv"),
                          ("drawdown_position_size_matr_two_origin.csv", "drawdown_position_size_matr_two_results.csv")])
def test_compute_drawdown_position_size_matr(drawdown_size_origin, drawdown_size_results):

    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                               "outputs_origin", "drawdown_position_size_matr_one_origin.csv"))
    path_results = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                                "outputs_to_test", "drawdown_position_size_matr_one_results.csv"))

    d_size_results = pd.read_csv(path_results, sep=',', engine='python')
    d_size_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(d_size_results.values.tolist()), np.array(d_size_origin.values.tolist())) is True


@pytest.mark.parametrize("limits_controls_origin, limits_controls_results",
                         [("limits_controls_one_origin.csv", "limits_controls_one_results.csv"),
                          ("limits_controls_two_origin.csv", "limits_controls_two_results.csv")])
def test_compute_limits_controls(limits_controls_origin, limits_controls_results):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                               "outputs_origin", limits_controls_origin))
    path_results = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                                "outputs_to_test", limits_controls_results))

    limits_results = pd.read_csv(path_results, sep=',', engine='python')
    limits_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(limits_results.values.tolist()), np.array(limits_origin.values.tolist())) is True
