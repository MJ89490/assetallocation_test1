from pathlib import Path

import pytest
import pandas as pd
import os

from assetallocation_arp.models import arp_signals
from assetallocation_arp.data_etl.dal.data_models.strategy import Times

CURRENT_PATH = Path(__file__).parent
TEST_PATH = os.path.abspath(os.path.join(CURRENT_PATH, "resources", "times"))


@pytest.mark.parametrize("index_data, inputs, week_day, expected_output",
                        [(pd.read_csv(f'{TEST_PATH}/index_data', header=0, index_col=0, parse_dates=True),
                          pd.read_csv(f'{TEST_PATH}/inputs', header=0, index_col=0, parse_dates=True),
                        1, pd.read_csv(f'{TEST_PATH}/signals', header=0, index_col=0, parse_dates=True))]
                        )
def test_momentum(index_data, inputs, week_day, expected_output):
    t = Times(week_day, inputs['frequency'].iat[0], inputs['leverage_type'].iat[0],
              [inputs['sig1_long'].iat[0], inputs['sig2_long'].iat[0], inputs['sig3_long'].iat[0]],
              [inputs['sig1_short'].iat[0], inputs['sig2_short'].iat[0], inputs['sig3_short'].iat[0]],
              inputs['time_lag'].iat[0], inputs['volatility_window'].iat[0])
    returns = arp_signals.momentum(index_data, t)
    pd.testing.assert_frame_equal(returns, expected_output)
