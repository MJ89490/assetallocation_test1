from pytest import raises, mark

from assetallocation_arp.data_etl.dal.data_models.strategy import Strategy, Times, Effect
from tests.assetallocation_arp.data_etl.dal.resources import valid_effect, valid_times

def test_times_day_of_week_setter_raises_key_error_invalid_day_of_week(valid_times):
    with raises(ValueError):
        Times(10, valid_times.frequency, valid_times.leverage_type, valid_times.long_signals, valid_times.short_signals,
              valid_times.time_lag_in_months, valid_times.volatility_window)


def test_times_day_of_week_setter_sets_day_of_week_valid_day_of_week(valid_times):
    day_of_week = 0

    a = Times(day_of_week, valid_times.frequency, valid_times.leverage_type, valid_times.long_signals,
              valid_times.short_signals, valid_times.time_lag_in_months, valid_times.volatility_window)

    assert a.day_of_week.value == day_of_week


def test_times_frequency_setter_raises_key_error_invalid_frequency(valid_times):
    with raises(KeyError):
        Times(valid_times.day_of_week, 'invalid_frequency', valid_times.leverage_type, valid_times.long_signals,
              valid_times.short_signals, valid_times.time_lag_in_months, valid_times.volatility_window)


def test_times_frequency_setter_sets_frequency_valid_frequency(valid_times):
    frequency = 'weekly'

    a = Times(valid_times.day_of_week, frequency, valid_times.leverage_type, valid_times.long_signals,
              valid_times.short_signals, valid_times.time_lag_in_months, valid_times.volatility_window)

    assert a.frequency.name == frequency


def test_leverage_type_setter_raises_key_error_invalid_leverage_type(valid_times):
    with raises(KeyError):
        Times(valid_times.day_of_week, valid_times.frequency, 'invalid_leverage_type', valid_times.long_signals,
              valid_times.short_signals, valid_times.time_lag_in_months, valid_times.volatility_window)


def test_leverage_type_setter_sets_leverage_type_valid_leverage_type(valid_times):
    leverage_type = 'e'

    a = Times(valid_times.day_of_week, valid_times.frequency, leverage_type, valid_times.long_signals,
              valid_times.short_signals, valid_times.time_lag_in_months, valid_times.volatility_window)

    assert a.leverage_type.name == leverage_type


@mark.parametrize('time_lag_in_months, expected', [(0, '0 mons'), (-5, '5 mons'), (3, '-3 mons')])
def test_time_lag_interval_property_gets_time_lag_interval_based_on_time_lag_in_months(time_lag_in_months, expected,
                                                                                       valid_times):
    a = Times(valid_times.day_of_week, valid_times.frequency, valid_times.leverage_type, valid_times.long_signals,
              valid_times.short_signals, time_lag_in_months, valid_times.volatility_window)
    assert expected == a.time_lag_interval



def test_carry_type_setter_raises_key_error_invalid_carry_type(valid_effect):
    e = Effect(*valid_effect)
    with raises(KeyError):
        e.carry_type = 'invalid_carry_type'


def test_carry_type_setter_sets_carry_type_valid_carry_type(valid_effect):
    e = Effect(*valid_effect)

    assert e.carry_type.name == valid_effect.carry_type


def test_effect_day_of_week_setter_raises_key_error_invalid_day_of_week(valid_effect):
    e = Effect(*valid_effect)
    with raises(ValueError):
        e.day_of_week = 10


def test_effect_day_of_week_setter_sets_day_of_week_valid_day_of_week(valid_effect):
    e = Effect(*valid_effect)
    assert e.day_of_week.value == valid_effect.day_of_week


def test_effect_frequency_setter_raises_key_error_invalid_frequency(valid_effect):
    e = Effect(*valid_effect)
    with raises(KeyError):
        e.frequency = 'invalid_frequency'


def test_effect_frequency_setter_sets_frequency_valid_frequency(valid_effect):
    e = Effect(*valid_effect)
    assert e.frequency.name == valid_effect.frequency


def test_trend_indicator_setter_raises_key_error_invalid_trend_indicator(valid_effect):
    e = Effect(*valid_effect)
    with raises(KeyError):
        e.trend_indicator = 'invalid_trend_indicator'


def test_trend_indicator_setter_sets_trend_indicator_valid_trend_indicator(valid_effect):
    e = Effect(*valid_effect)
    assert e.trend_indicator.name == valid_effect.trend_indicator
