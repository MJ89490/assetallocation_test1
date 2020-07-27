import os
import numpy as np
import pandas as pd

PATH_ORIGIN = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                              "trades_overview_origin.csv"))
PATH_RESULTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                               "trades_overview_results.csv"))
TRADES_RESULTS = pd.read_csv(PATH_RESULTS, sep=',', engine='python')
TRADES_ORIGIN = pd.read_csv(PATH_ORIGIN, sep=',', engine='python')


def test_compute_signals_real_carry():
    assert np.allclose(np.array(TRADES_RESULTS.This_week.tolist()),
                       np.array(TRADES_ORIGIN.This_week.tolist())) is True
