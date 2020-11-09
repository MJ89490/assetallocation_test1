from pathlib import Path

from assetallocation_arp.models import maven
from tests.assetallocation_arp.models.resources.helper import read_inputs_outputs, assert_equal

resource_path = Path(__file__).parent / 'resources' / 'maven'


def test_format_data():
    test_kwargs, expected = read_inputs_outputs(resource_path / 'format_data')
    returns = maven.format_data(**test_kwargs)

    if isinstance(returns, tuple):
        for counter, v in enumerate(returns):
            assert_equal(str(counter), expected, v)

    else:
        assert_equal('0', expected, returns)


def test_calculate_excess_returns():
    test_kwargs, expected = read_inputs_outputs(resource_path / 'calculate_excess_returns')
    returns = maven.calculate_excess_returns(**test_kwargs)

    if isinstance(returns, tuple):
        for counter, v in enumerate(returns):
            assert_equal(str(counter), expected, v)

    else:
        assert_equal('0', expected, returns)


def test_calculate_signals():
    test_kwargs, expected = read_inputs_outputs(resource_path / 'calculate_signals')
    returns = maven.calculate_signals(**test_kwargs)

    if isinstance(returns, tuple):
        for counter, v in enumerate(returns):
            assert_equal(str(counter), expected, v)

    else:
        assert_equal('0', expected, returns)


def test_run_performance_stats():
    test_kwargs, expected = read_inputs_outputs(resource_path / 'run_performance_stats')
    returns = maven.run_performance_stats(**test_kwargs)

    if isinstance(returns, tuple):
        for counter, v in enumerate(returns):
            assert_equal(str(counter), expected, v)

    else:
        assert_equal('0', expected, returns)
