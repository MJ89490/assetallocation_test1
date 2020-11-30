import os
import pytest
import numpy as np
import pandas as pd

"""
Notes: 
one: total return; 4 ;16; Yes; 2.0; 0.0; real; yes; 0.25; 1/N; 52; 10; 4
two: spot; 4 ;16; No; 2.0; 0.0; real; yes; 0.25 ;1/N ;52 ;10 ;4
"""


@pytest.mark.parametrize("profit_and_loss_overview_origin, profit_and_loss_overview_results",
                         [("profit_and_loss_overview_one_origin.csv", "profit_and_loss_overview_one_results.csv"),
                          ("profit_and_loss_overview_two_origin.csv", "profit_and_loss_overview_two_results.csv")])
def test_compute_profit_and_loss_combo(profit_and_loss_overview_origin, profit_and_loss_overview_results):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                                               profit_and_loss_overview_origin))
    path_results = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                                                profit_and_loss_overview_results))

    profit_and_loss_results = pd.read_csv(path_results, sep=',', engine='python')
    profit_and_loss_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(profit_and_loss_results.Last_week.tolist()),
                       np.array(profit_and_loss_origin.Last_week.tolist())) is True


@pytest.mark.parametrize("profit_and_loss_overview_origin, profit_and_loss_overview_results",
                         [("profit_and_loss_overview_one_origin.csv", "profit_and_loss_overview_one_results.csv"),
                          ("profit_and_loss_overview_two_origin.csv", "profit_and_loss_overview_two_results.csv")])
def test_compute_profit_and_loss_returns(profit_and_loss_overview_origin, profit_and_loss_overview_results):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                                               profit_and_loss_overview_origin))
    path_results = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                                                profit_and_loss_overview_results))

    profit_and_loss_results = pd.read_csv(path_results, sep=',', engine='python')
    profit_and_loss_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(profit_and_loss_results.Total.tolist()),
                       np.array(profit_and_loss_origin.Total.tolist())) is True


@pytest.mark.parametrize("profit_and_loss_overview_origin, profit_and_loss_overview_results",
                         [("profit_and_loss_overview_one_origin.csv", "profit_and_loss_overview_one_results.csv"),
                          ("profit_and_loss_overview_two_origin.csv", "profit_and_loss_overview_two_results.csv")])
def test_compute_profit_and_loss_spot(profit_and_loss_overview_origin, profit_and_loss_overview_results):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                                               profit_and_loss_overview_origin))
    path_results = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                                                profit_and_loss_overview_results))

    profit_and_loss_results = pd.read_csv(path_results, sep=',', engine='python')
    profit_and_loss_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(profit_and_loss_results.Spot.tolist()),
                       np.array(profit_and_loss_origin.Spot.tolist())) is True


@pytest.mark.parametrize("profit_and_loss_overview_origin, profit_and_loss_overview_results",
                         [("profit_and_loss_overview_one_origin.csv", "profit_and_loss_overview_one_results.csv"),
                          ("profit_and_loss_overview_two_origin.csv", "profit_and_loss_overview_two_results.csv")])
def test_compute_profit_and_loss_carry(profit_and_loss_overview_origin, profit_and_loss_overview_results):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                                               profit_and_loss_overview_origin))
    path_results = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                                                profit_and_loss_overview_results))

    profit_and_loss_results = pd.read_csv(path_results, sep=',', engine='python')
    profit_and_loss_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(profit_and_loss_results.Carry.tolist()),
                       np.array(profit_and_loss_origin.Carry.tolist())) is True


@pytest.mark.parametrize("profit_and_loss_overview_origin, profit_and_loss_overview_results",
                         [("profit_and_loss_notional_one_origin.csv", "profit_and_loss_notional_one_results.csv"),
                          ("profit_and_loss_notional_two_origin.csv", "profit_and_loss_notional_two_results.csv")])
def test_compute_profit_and_loss_notional(profit_and_loss_overview_origin, profit_and_loss_overview_results):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                               "outputs_origin", profit_and_loss_overview_origin))
    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                               "outputs_to_test", profit_and_loss_overview_results))

    notional_results = pd.read_csv(path_result, sep=',', engine='python')
    notional_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(notional_origin.values), np.array(notional_results.values)) is True


@pytest.mark.parametrize("profit_and_loss_overview_origin, profit_and_loss_overview_results",
                         [("profit_and_loss_matr_one_origin.csv", "profit_and_loss_matr_one_results.csv"),
                          ("profit_and_loss_matr_two_origin.csv", "profit_and_loss_matr_two_results.csv")])
def test_compute_profit_and_loss_implemented_in_matr(profit_and_loss_overview_origin, profit_and_loss_overview_results):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                               "outputs_origin", profit_and_loss_overview_origin))
    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources","effect",
                                               "outputs_to_test", profit_and_loss_overview_results))

    matr_results = pd.read_csv(path_result, sep=',', engine='python')
    matr_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(matr_origin.values), np.array(matr_results.values)) is True

