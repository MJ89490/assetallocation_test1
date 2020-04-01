from pathlib import Path

import pytest
import pandas as pd
import os

from assetallocation_arp.models import arp_signals

CURRENT_PATH = Path(__file__).parent
TEST_PATH = os.path.abspath(os.path.join(CURRENT_PATH, "resources", "times"))


@pytest.mark.parametrize("index_data, inputs, week_day, expected_output",
                        [(pd.read_csv(f'{TEST_PATH}/index_data', header=0, index_col=0, parse_dates=True),
                          pd.read_csv(f'{TEST_PATH}/inputs', header=0, index_col=0, parse_dates=True),
                        'TUE', pd.read_csv(f'{TEST_PATH}/signals', header=0, index_col=0, parse_dates=True))]
                        )
def test_momentum(index_data, inputs, week_day, expected_output):
    returns = arp_signals.momentum(index_data, inputs, week_day)
    pd.testing.assert_frame_equal(returns, expected_output)
