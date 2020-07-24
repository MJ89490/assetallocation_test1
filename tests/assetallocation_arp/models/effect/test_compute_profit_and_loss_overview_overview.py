import os
import numpy as np
import pandas as pd

PATH_ORIGIN = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                              "profit_and_loss_overview_origin.csv"))
PATH_RESULTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                               "profit_and_loss_overview_results.csv"))
PROFIT_AND_LOSS_RESULTS = pd.read_csv(PATH_RESULTS, sep=',', engine='python')
PROFIT_AND_LOSS_ORIGIN = pd.read_csv(PATH_ORIGIN, sep=',', engine='python')


def test_compute_profit_and_loss_combo():
    assert np.allclose(np.array(PROFIT_AND_LOSS_RESULTS.Last_week.tolist()),
                       np.array(PROFIT_AND_LOSS_ORIGIN.Last_week.tolist())) is True


def test_compute_profit_and_loss_returns():
    assert np.allclose(np.array(PROFIT_AND_LOSS_RESULTS.Total.tolist()),
                       np.array(PROFIT_AND_LOSS_ORIGIN.Total.tolist())) is True


def test_compute_profit_and_loss_spot():
    assert np.allclose(np.array(PROFIT_AND_LOSS_RESULTS.Spot.tolist()),
                       np.array(PROFIT_AND_LOSS_ORIGIN.Spot.tolist())) is True


def test_compute_profit_and_loss_carry():
    assert np.allclose(np.array(PROFIT_AND_LOSS_RESULTS.Carry.tolist()),
                       np.array(PROFIT_AND_LOSS_ORIGIN.Carry.tolist())) is True