import os
import numpy as np
import pandas as pd

PATH_ORIGIN = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                              "risk_returns_table_origin.csv"))
PATH_RESULTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                               "risk_returns_table_results.csv"))
RISK_RETURNS_RESULTS = pd.read_csv(PATH_RESULTS, sep=',', engine='python')
RISK_RETURNS_ORIGIN = pd.read_csv(PATH_ORIGIN, sep=',', engine='python')


def test_compute_excess_returns():
    assert np.allclose(np.array(RISK_RETURNS_RESULTS.excess_returns_with_signals.values),
                       np.array(RISK_RETURNS_ORIGIN.excess_returns_with_signals.values)) is True

    assert np.allclose(np.array(RISK_RETURNS_RESULTS.excess_returns_no_signals.values),
                       np.array(RISK_RETURNS_ORIGIN.excess_returns_no_signals.values)) is True


def test_compute_std_dev():
    assert np.allclose(np.array(RISK_RETURNS_RESULTS.std_dev_with_signals.values),
                       np.array(RISK_RETURNS_ORIGIN.std_dev_with_signals.values)) is True

    assert np.allclose(np.array(RISK_RETURNS_RESULTS.std_dev_no_signals.values),
                       np.array(RISK_RETURNS_ORIGIN.std_dev_no_signals.values)) is True


def test_compute_sharpe_ratio():
    assert np.allclose(np.array(RISK_RETURNS_RESULTS.sharpe_with_signals.values),
                       np.array(RISK_RETURNS_ORIGIN.sharpe_with_signals.values)) is True

    assert np.allclose(np.array(RISK_RETURNS_RESULTS.sharpe_no_signals.values),
                       np.array(RISK_RETURNS_ORIGIN.sharpe_no_signals.values)) is True


def test_compute_max_drawdown():
    assert np.allclose(np.array(RISK_RETURNS_RESULTS.max_drawdown_with_signals.values),
                       np.array(RISK_RETURNS_ORIGIN.max_drawdown_with_signals.values)) is True

    assert np.allclose(np.array(RISK_RETURNS_RESULTS.max_drawdown_no_signals.values),
                       np.array(RISK_RETURNS_ORIGIN.max_drawdown_no_signals.values)) is True





def test_compute_calmar_ratio():
    pass
