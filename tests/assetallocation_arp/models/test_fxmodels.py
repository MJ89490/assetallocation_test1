from pathlib import Path

from assetallocation_arp.models import fxmodels as fx
from tests.assetallocation_arp.models.resources.helper import read_inputs_outputs, assert_equal

resource_path = Path(__file__).parent / 'resources' / 'fxmodels'


def test_create_sizing_mapping():
    test_kwargs, expected = read_inputs_outputs(resource_path / 'create_sizing_map')

    returns = fx.create_sizing_mapping(**test_kwargs)

    if isinstance(returns, tuple):
        for counter, v in enumerate(returns):
            assert_equal(str(counter), expected, v)

    else:
        assert_equal('0', expected, returns)
