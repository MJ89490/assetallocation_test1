import os
import numpy as np
import pandas as pd

"""
Notes: 
one: total return; 4 ;16; Yes; 2.0; 0.0; real; yes; 0.25; 1/N; 52; 10; 4

"""

PATH_ORIGIN = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                              "signals_overview_one_origin.csv"))
PATH_RESULTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                               "signals_overview_one_results.csv"))
SIGNALS_RESULTS = pd.read_csv(PATH_RESULTS, sep=',', engine='python')
SIGNALS_ORIGIN = pd.read_csv(PATH_ORIGIN, sep=',', engine='python')


def test_compute_signals_real_carry():
    assert np.allclose(np.array(SIGNALS_RESULTS.Real_carry.tolist()),
                       np.array(SIGNALS_ORIGIN.Real_carry.tolist())) is True


def test_compute_signals_trend():
    assert np.allclose(np.array(SIGNALS_RESULTS.Trend.tolist()),
                       np.array(SIGNALS_ORIGIN.Trend.tolist())) is True


def test_compute_signals_combo():
    assert np.allclose(np.array(SIGNALS_RESULTS.This_week.tolist()),
                       np.array(SIGNALS_ORIGIN.This_week.tolist())) is True


def test_compute_drawdown_position_size_matr():
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                               "outputs_origin", "drawdown_position_size_matr_one_origin.csv"))
    path_results = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                                "outputs_to_test", "drawdown_position_size_matr_one_results.csv"))

    drawdown_size_results = pd.read_csv(path_results, sep=',', engine='python')
    drawdown_size_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(drawdown_size_results.values.tolist()), np.array(drawdown_size_origin.values.tolist())) is True


def test_compute_limits_controls():
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                               "outputs_origin", "limits_controls_one_origin.csv"))
    path_results = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                                "outputs_to_test", "limits_controls_one_results.csv"))

    limits_results = pd.read_csv(path_results, sep=',', engine='python')
    limits_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(limits_results.values.tolist()), np.array(limits_origin.values.tolist())) is True
