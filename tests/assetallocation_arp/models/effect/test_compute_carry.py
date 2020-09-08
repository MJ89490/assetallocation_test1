import os
import pandas as pd
import numpy as np
import pytest

@pytest.fixture
def currencies():
    return ['BRL', 'TRY', 'THB']


@pytest.mark.parametrize("carry_origin, carry_results",
                         [("carry_one_origin.csv", "carry_one_results.csv")])
def test_compute_carry(currencies, carry_origin, carry_results):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                                               carry_origin))
    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                                               carry_results))

    carry_results = pd.read_csv(path_result, sep=',', engine='python')
    carry_origin = pd.read_csv(path_origin, sep=',', engine='python')

    for currency in currencies:
        assert np.allclose(np.array(carry_results[currency].tolist()), np.array(carry_origin[currency].tolist())) is True
