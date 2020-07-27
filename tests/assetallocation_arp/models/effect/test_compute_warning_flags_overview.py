import os
import numpy as np
import pandas as pd

PATH_ORIGIN = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                              "warning_flags_overview_origin.csv"))
PATH_RESULTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                               "warning_flags_overview_results.csv"))
WARNING_FLAGS_RESULTS = pd.read_csv(PATH_RESULTS, sep=',', engine='python')
WARNING_FLAGS_ORIGIN = pd.read_csv(PATH_ORIGIN, sep=',', engine='python')


def test_compute_warning_flags_rates():
    assert np.allclose(np.array(WARNING_FLAGS_RESULTS.Rates.tolist()),
                       np.array(WARNING_FLAGS_ORIGIN.Rates.tolist())) is True
