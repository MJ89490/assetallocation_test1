"""
Created on 13/01/2019
Author: AJ89720
email: Anais.Jeremie@lgim.com
"""

import pytest
import os
import pandas as pd

from assetallocation_arp.data_etl import import_data as data

CURRENT_PATH = os.path.dirname(__file__)

"""
Module test_import_data.py: tests the extract data method (import_data.py) in order to know if it returns the correct 
following outputs:
    - strategy_inputs
    - asset_inputs
    - all_data (we assume they are the correct data because we can't test the matlab file, it is very heavy)
"""

@pytest.mark.parametrize("model_type, mat_file, input_file, model_date, strategy_inputs_expected, asset_inputs_expected",
                         [('times', None, None, None,
                           os.path.abspath(os.path.join(CURRENT_PATH, "resources", "strategy_inputs_expected")),
                           os.path.abspath(os.path.join(CURRENT_PATH, "resources", "asset_inputs_expected"))
                           )]
                         )
def test_extract_inputs_and_mat_data(model_type, mat_file, input_file, model_date, strategy_inputs_expected,
                                     asset_inputs_expected):

    dataframe_strategy_inputs = pd.read_csv(strategy_inputs_expected, index_col=0)
    dataframe_asset_inputs = pd.read_csv(asset_inputs_expected, index_col=0)

    strategy_inputs_origin, asset_inputs_origin, all_data = data.extract_inputs_and_mat_data(model_type=model_type,
                                                                                             mat_file=mat_file,
                                                                                             input_file=input_file,
                                                                                             model_date=model_date)
    pd.testing.assert_frame_equal(strategy_inputs_origin,
                                      dataframe_strategy_inputs, check_column_type=False, check_names=False, check_dtype=False)

    pd.testing.assert_frame_equal(asset_inputs_origin,
                                      dataframe_asset_inputs, check_column_type=False, check_names=False, check_dtype=False)
