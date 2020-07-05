import os
import pandas as pd
import numpy as np
import pytest


@pytest.mark.parametrize("currency, carry_origin, carry_results",
                        [("BRL", "brl_carry_origin.csv", "brl_carry_results.csv"),
                         ("MXN", "mxn_carry_origin.csv", "mxn_carry_results.csv"),
                         ("COP", "cop_carry_origin.csv", "cop_carry_results.csv"),
                         # ("CLP", "clp_carry_origin.csv", "clp_carry_results.csv"),
                         # ("PEN", "pen_carry_origin.csv", "pen_carry_results.csv"),
                         # ("TRY", "try_carry_origin.csv", "try_carry_results.csv"),
                         # ("RUB", "rub_carry_origin.csv", "rub_cary_results.csv"),
                         # ("ZAR", "zar_carry_origin.csv", "zar_carry_results.csv"),
                         # ("CNY", "cny_carry_origin.csv", "cny_carry_results.csv"),
                         # ("KRW", "krw_carry_origin.csv", "krw_carry_results.csv"),
                         # ("MYR", "myr_carry_origin.csv", "myr_carry_results.csv"),
                         # ("IDR", "idr_carry_origin.csv", "idr_carry_results.csv"),
                         # ("INR", "inr_carry_origin.csv", "inr_carry_results.csv"),
                         # ("PHP", "php_carry_origin.csv", "php_carry_results.csv"),
                         # ("TWD", "twd_carry_origin.csv", "twd_carry_results.csv"),
                         # ("THB", "thb_carry_origin.csv", "thb_carry_results.csv")
                         ])
def test_compute_carry(currency, carry_origin, carry_results):
    path_origin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin",
                                               "carry_origin", carry_origin))
    path_result = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_to_test",
                                               "carry_results", carry_results))

    carry_results = pd.read_csv(path_result, sep=',', engine='python')
    carry_origin = pd.read_csv(path_origin, sep=',', engine='python')

    assert np.allclose(np.array(carry_results[currency].tolist()), np.array(carry_origin[currency].tolist())) is True

#erreur 27/03/2020 implied valeur