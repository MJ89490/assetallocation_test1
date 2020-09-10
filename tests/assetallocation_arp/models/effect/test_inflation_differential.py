import os
import pandas as pd
import numpy as np
import pytest


@pytest.fixture
def currencies():
    return ['BRL', 'TRY', 'THB']


def test_compute_inflation_release():
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                               "outputs_origin", "inflation_release_origin.csv"))
    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                               "outputs_to_test", "inflation_release_results.csv"))

    inflation_results = pd.read_csv(path_result, sep=',', engine='python')
    inflation_origin = pd.read_csv(path_origin, sep=',', engine='python')

    pd.testing.assert_series_equal(inflation_results.Inflation_Release, inflation_origin.Inflation_Release)


def test_compute_inflation_differential(currencies):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                               "outputs_origin", "inflation_differential_origin.csv"))
    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect",
                                               "outputs_to_test", "inflation_differential_results.csv"))

    inflation_results = pd.read_csv(path_result, sep=',', engine='python')
    inflation_origin = pd.read_csv(path_origin, sep=',', engine='python')

    for currency in currencies:
        assert np.allclose(np.array(inflation_results[currency].tolist()), np.array(inflation_origin[currency].tolist())) is True


