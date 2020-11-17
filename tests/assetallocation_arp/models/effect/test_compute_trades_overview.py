import os
import pytest
import numpy as np
import pandas as pd

"""
Notes: 
one: total return; 4 ;16; Yes; 2.0; 0.0; real; yes; 0.25; 1/N; 52; 10; 4
two: spot; 4 ;16; No; 2.0; 0.0; real; yes; 0.25 ;1/N ;52 ;10 ;4
"""


@pytest.mark.parametrize("trades_overview_origin, trades_overview_results",
                         [("trades_overview_one_origin.csv", "trades_overview_one_results.csv"),
                          ("trades_overview_two_origin.csv", "trades_overview_two_results.csv")])
def test_compute_trades_overview(trades_overview_origin, trades_overview_results):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                                               "trades_overview_one_origin.csv"))
    path_results = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                     "trades_overview_one_results.csv"))
    trades_results = pd.read_csv(path_results, sep=',', engine='python')
    trades_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(trades_origin.This_week.tolist()), np.array(trades_results.This_week.tolist())) is True
