from _pydecimal import Decimal
from collections import namedtuple

from _pytest.fixtures import fixture


@fixture
def valid_times():
    TimesInput = namedtuple('TimesInput', ['day_of_week', 'frequency', 'leverage_type', 'long_signals', 'short_signals',
                                           'time_lag_in_months', 'volatility_window', 'description', 'time_lag_interval'])
    return TimesInput(0, 'weekly', 'e', [], [], 1, 1, '', '-1 mons')


@fixture
def valid_effect():
    EffectInput = namedtuple('EffectInput',
                             ['carry_type', 'closing_threshold', 'cost', 'day_of_week', 'frequency', 'include_shorts',
                              'inflation_lag_in_months', 'interest_rate_cut_off_long', 'interest_rate_cut_off_short',
                              'moving_average_long_term', 'moving_average_short_term', 'is_realtime_inflation_forecast',
                              'trend_indicator'])
    return EffectInput('Nominal', Decimal(1), Decimal(1), 0, 'weekly', True, 1, Decimal(1), Decimal(1), 1, 1, True,
                       'TotalReturn')