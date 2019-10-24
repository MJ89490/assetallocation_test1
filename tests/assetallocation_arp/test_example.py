import os
import sys
import pytest

# Explicitly set path so don't need to run setup.py - if we have multiple copies of the code we would otherwise need
# to setup a separate environment for each to ensure the code pointers are correct.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # noqa

# from pandas.util.testing import assert_frame_equal
from assetallocation_arp.assetallocation_arp.data_etl import make_dataset


@pytest.mark.parametrize("input_filepath, output_filepath, expected_output",
                         [('c:/abc/1/inputs/file1.csv', 'c:/abc/1/outputs/','out_filename1'),
                          ('c:/abc/1/inputs/file2.csv', 'c:/abc/1/outputs/','out_filename2'),
                          ('', 'c:/abc/1/outputs/','out_filename2'),
                          ('c:/abc/1/inputs/file2.csv', '','out_filename2'),
                          ('', '','')
                         ])
def test_data_etl_main(input_filepath, output_filepath, expected_output):
    """
    :param input_filepath: string, input data_file path
    :param output_filepath: df in output_file
    :return: tests the method dataetl_main
    """
    actual_output = make_dataset(input_filepath, output_filepath)
    assert actual_output == expected_output"
