from collections import namedtuple

from _pytest.fixtures import fixture
from psycopg2.extras import DateTimeTZRange
from psycopg2.tz import FixedOffsetTimezone
import datetime as dt

@fixture
def valid_times():
    TimesInput = namedtuple('TimesInput', ['day_of_week', 'frequency', 'leverage_type', 'long_signals', 'short_signals',
                                           'time_lag_in_months', 'volatility_window', 'description', 'time_lag_interval'])
    return TimesInput(0, 'weekly', 'e', [], [], 1, 1, '', '-1 mons')


@fixture
def valid_effect():
    EffectInput = namedtuple(
        'EffectInput', [
            'update_imf', 'user_date', 'signal_date', 'position_size', 'risk_weighting', 'st_dev_window',
            'bid_ask_spread', 'carry_type', 'closing_threshold', 'day_of_week', 'frequency', 'include_shorts',
            'interest_rate_cut_off_long', 'interest_rate_cut_off_short', 'moving_average_long_term',
            'moving_average_short_term', 'is_real_time_inflation_forecast', 'trend_indicator'])
    return EffectInput(
        True, dt.date(2020, 1, 1), dt.date(2020, 1, 1), float(1), '1/N', 1, 1, 'Nominal', float(1), 0, 'weekly', True,
        float(1), float(1), 1, 1, True, 'Total return')


@fixture
def valid_fica():
    FicaInput = namedtuple('FicaInput', ['description', 'coupon', 'curve', 'business_tstzrange', 'strategy_weights',
                                         'tenor', 'trading_cost'])
    return FicaInput('a', 1.0, 'e', DateTimeTZRange(dt.datetime(2020, 1, 1, tzinfo=FixedOffsetTimezone(offset=0, name=None)),
                                                    dt.datetime(2020, 2, 2, tzinfo=FixedOffsetTimezone(offset=0, name=None)), bounds='[)'), [1, 2], 1, 1)


@fixture
def valid_times_asset():
    TimesAssetInput = namedtuple('TimesAssetInput', ['ticker', 'category', 'country', 'currency', 'name',
                                           'type', 's_leverage', 'signal_ticker', 'future_ticker', 'cost'])
    return TimesAssetInput('test_ticker', 'Equity', 'US', 'EUR', 'test_name', 'b', 2, 'f', 'g', float(1))
