from collections import namedtuple

from _pytest.fixtures import fixture


@fixture
def valid_times():
    TimesInput = namedtuple('TimesInput', ['day_of_week', 'frequency', 'leverage_type', 'long_signals', 'short_signals',
                                           'time_lag_in_days', 'volatility_window', 'description', 'time_lag_interval'])
    return TimesInput(0, 'weekly', 'e', [], [], 1, 1, '', '-1 mons')


@fixture
def valid_effect():
    EffectInput = namedtuple('EffectInput',
                             ['carry_type', 'closing_threshold', 'cost', 'day_of_week', 'frequency', 'include_shorts',
                              'inflation_lag_in_months', 'interest_rate_cut_off_long', 'interest_rate_cut_off_short',
                              'moving_average_long_term', 'moving_average_short_term', 'is_realtime_inflation_forecast',
                              'trend_indicator'])
    return EffectInput('Nominal', float(1), float(1), 0, 'weekly', True, 1, float(1), float(1), 1, 1, True,
                       'TotalReturn')


@fixture
def valid_fica():
    FicaInput = namedtuple('FicaInput', ['description', 'coupon', 'curve', 'strategy_weights',
                                         'tenor', 'trading_cost'])
    return FicaInput('a', 1.0, 'e', [1, 2], 1, 1)


@fixture
def valid_times_asset():
    TimesAssetInput = namedtuple('TimesAssetInput', ['ticker', 'category', 'country', 'currency', 'name',
                                           'type', 's_leverage', 'signal_ticker', 'future_ticker', 'cost'])
    return TimesAssetInput('test_ticker', 'Equity', 'US', 'EUR', 'test_name', 'b', 2, 'f', 'g', float(1))
