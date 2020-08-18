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


def test_format_data():
    test_kwargs, expected = read_inputs_outputs(resource_path / 'format_data')
    returns = fx.format_data(**test_kwargs)

    if isinstance(returns, tuple):
        for counter, v in enumerate(returns):
            assert_equal(str(counter), expected, v)

    else:
        assert_equal('0', expected, returns)


def test_calculate_signals():
    test_kwargs, expected = read_inputs_outputs(resource_path / 'calculate_signals')
    returns = fx.calculate_signals(**test_kwargs)

    if isinstance(returns, tuple):
        for counter, v in enumerate(returns):
            assert_equal(str(counter), expected, v)

    else:
        assert_equal('0', expected, returns)


def test_determine_sizing():
    test_kwargs, expected = read_inputs_outputs(resource_path / 'determine_sizing')
    returns = fx.determine_sizing(**test_kwargs)

    if isinstance(returns, tuple):
        for counter, v in enumerate(returns):
            assert_equal(str(counter), expected, v)

    else:
        assert_equal('0', expected, returns)


def test_calculate_returns():
    test_kwargs, expected = read_inputs_outputs(resource_path / 'calculate_returns')
    returns = fx.calculate_returns(**test_kwargs)

    if isinstance(returns, tuple):
        for counter, v in enumerate(returns):
            assert_equal(str(counter), expected, v)

    else:
        assert_equal('0', expected, returns)

"""
fxmodels_inputs, asset_inputs, all_data = gd.extract_inputs_and_mat_data(model_type, mat_file, input_file)
        spot, carry, cash, ppp = fxmodels.format_data(fxmodels_inputs, asset_inputs, all_data)
        signal, volatility = fxmodels.calculate_signals(fxmodels_inputs, spot, carry, cash, ppp)
        fx_model, exposure, exposure_agg = fxmodels.determine_sizing(fxmodels_inputs, asset_inputs, signal, volatility)
        base_fx, returns, contribution, carry_base = fxmodels.calculate_returns(fxmodels_inputs, carry, signal,
                                                                                exposure, exposure_agg)
        return base_fx, returns, contribution, carry_base
        
       """