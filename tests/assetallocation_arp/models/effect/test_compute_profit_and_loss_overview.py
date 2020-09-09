import os
import numpy as np
import pandas as pd

"""
Notes: 
one: total return; 4 ;16; Yes; 2.0; 0.0; real; yes; 0.25; 1/N; 52; 10; 4

"""

PATH_ORIGIN = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                              "profit_and_loss_overview_one_origin.csv"))
PATH_RESULTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                               "profit_and_loss_overview_one_results.csv"))
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


def test_compute_profit_and_loss_notional():
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                               "outputs_origin", "profit_and_loss_notional_one_origin.csv"))
    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                               "outputs_to_test", "profit_and_loss_notional_one_results.csv"))

    notional_results = pd.read_csv(path_result, sep=',', engine='python')
    notional_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(notional_origin.values), np.array(notional_results.values)) is True


def test_compute_profit_and_loss_implemented_in_matr():
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                               "outputs_origin", "profit_and_loss_matr_one_origin.csv"))
    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources",
                                               "effect", "outputs_to_test", "profit_and_loss_matr_one_results.csv"))

    matr_results = pd.read_csv(path_result, sep=',', engine='python')
    matr_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(matr_origin.values), np.array(matr_results.values)) is True

