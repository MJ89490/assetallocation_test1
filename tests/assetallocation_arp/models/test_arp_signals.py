from pathlib import Path

import pytest
import pandas as pd

from assetallocation_arp.models import arp_signals

test_path = Path(__file__).parent

@pytest.mark.parametrize("index_data, inputs, week_day, expected_output",
                        [(pd.read_csv(f'{test_path}\\index_data.csv', header=0, index_col=0, parse_dates=True),
                          pd.read_csv(f'{test_path}\\inputs.csv', header=0, index_col=0, parse_dates=True),
                        'TUE', pd.read_csv(f'{test_path}\\signal.csv', header=0, index_col=0, parse_dates=True))]
                        )
def test_momentum(index_data, inputs, week_day, expected_output):
    returns = arp_signals.momentum(index_data, inputs, week_day)
    pd.testing.assert_frame_equal(returns, expected_output)
