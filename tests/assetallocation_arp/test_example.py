import os
import sys
import pytest

# Explicitly set path so don't need to run setup.py - if we have multiple copies of the code we would otherwise need
# to setup a separate environment for each to ensure the code pointers are correct.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # noqa

# from pandas.util.testing import assert_frame_equal
from assetallocation_arp.data_etl.import_data import dataimport_future

@pytest.mark.parametrize("H:\\assetallocation_arp\\data\\raw\\Future data"
                          ('', '','')
                         )
def test_data_etl_main(file_name, expected_output):
    """
    :param input_filepath: string, input data_file path
    :param output_filepath: df in output_file
    :return: tests the method dataetl_main
    """
    actual_output = dataimport_future(file_name)
    assert actual_output == expected_output
