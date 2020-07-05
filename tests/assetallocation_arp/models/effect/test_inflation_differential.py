import os
import pandas as pd
import numpy as np
import pytest

def test_compute_inflation_release():
    path_origin = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "inflation_release_origin.csv"))
    path_result = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test", "inflation_release_results.csv"))

    inflation_results = pd.read_csv(path_result, sep=',', engine='python')
    inflation_origin = pd.read_csv(path_origin, sep=',', engine='python')

    pd.testing.assert_series_equal(inflation_results.Inflation_Release, inflation_origin.Inflation_Release)

@pytest.mark.parametrize("currency, inflation_differential_origin, inflation_differential_results",
                         [("BRL", "brl_inflation_differential_origin.csv", "brl_inflation_differential_results.csv"),
                          ("MXN", "mxn_inflation_differential_origin.csv", "mxn_inflation_differential_results.csv"),
                          ("COP", "cop_inflation_differential_origin.csv", "cop_inflation_differential_results.csv"),
                          ("CLP", "clp_inflation_differential_origin.csv", "clp_inflation_differential_results.csv"),
                          ("PEN", "pen_inflation_differential_origin.csv", "pen_inflation_differential_results.csv"),
                          ("TRY", "try_inflation_differential_origin.csv", "try_inflation_differential_results.csv"),
                          ("RUB", "rub_inflation_differential_origin.csv", "rub_inflation_differential_results.csv"),
                          ("ZAR", "zar_inflation_differential_origin.csv", "zar_inflation_differential_results.csv"),
                          ("CNY", "cny_inflation_differential_origin.csv", "cny_inflation_differential_results.csv"),
                          ("KRW", "krw_inflation_differential_origin.csv", "krw_inflation_differential_results.csv"),
                          ("MYR", "myr_inflation_differential_origin.csv", "myr_inflation_differential_results.csv"),
                          ("IDR", "idr_inflation_differential_origin.csv", "idr_inflation_differential_results.csv"),
                          ("INR", "inr_inflation_differential_origin.csv", "inr_inflation_differential_results.csv"),
                          ("PHP", "php_inflation_differential_origin.csv", "php_inflation_differential_results.csv"),
                          ("TWD", "twd_inflation_differential_origin.csv", "twd_inflation_differential_results.csv"),
                          ("THB", "thb_inflation_differential_origin.csv", "thb_inflation_differential_results.csv")
                          ])
def test_compute_inflation_differential(currency, inflation_differential_origin, inflation_differential_results):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "inflation_differential_origin", inflation_differential_origin))
    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test", "inflation_differential_results", inflation_differential_results))

    inflation_results = pd.read_csv(path_result, sep=',', engine='python')
    inflation_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(inflation_results[currency].tolist()), np.array(inflation_origin[currency].tolist())) is True


