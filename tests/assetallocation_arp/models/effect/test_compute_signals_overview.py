import os
import numpy as np
import pandas as pd

PATH_ORIGIN = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                              "signals_overview_origin.csv"))
PATH_RESULTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                               "signals_overview_results.csv"))
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