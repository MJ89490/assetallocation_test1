from pathlib import Path

import pandas as pd
from pytest import fixture

r_path = Path(__file__).parent / 'resources' / 'fica'

from assetallocation_arp.models import fica as f


@fixture
def fica_inputs():
    return pd.read_csv(r_path / 'fica_inputs.csv', index_col=0)


@fixture
def asset_inputs():
    return pd.read_csv(r_path / 'asset_inputs.csv', index_col=0)


@fixture
def all_data():
    ad = pd.read_csv(r_path / 'all_data.csv', index_col=0)
    index_ad = [pd.Timestamp(date) for date in ad.index.values]
    return ad.reindex(index_ad)  # reset the dates of the index to Timestamp


@fixture
def curve():
    c = pd.read_csv(r_path / 'curve.csv', index_col=0)
    index_c = [pd.Timestamp(date) for date in c.index.values]
    return c.reindex(index_c)  # reset the dates of the index to Timestamp

@fixture
def carry_roll():
    cr = pd.read_csv(r_path / 'carry_roll.csv', index_col=0)
    index_cr = [pd.Timestamp(date) for date in cr.index.values]
    return cr.reindex(index_cr)  # reset the dates of the index to Timestamp

@fixture
def country_returns():
    cr = pd.read_csv(r_path / 'country_returns.csv', index_col=0)
    index_cr = [pd.Timestamp(date) for date in cr.index.values]
    return cr.reindex(index_cr)  # reset the dates of the index to Timestamp


@fixture
def signals():
    s = pd.read_csv(r_path / 'signals.csv', index_col=0)
    index_s = [pd.Timestamp(date) for date in s.index.values]
    return s.reindex(index_s)  # reset the dates of the index to Timestamp


@fixture
def cum_contribution():
    cc = pd.read_csv(r_path / 'cum_contribution.csv', index_col=0)
    index_cc = [pd.Timestamp(date) for date in cc.index.values]
    return cc.reindex(index_cc)  # reset the dates of the index to Timestamp


@fixture
def returns():
    r = pd.read_csv(r_path / 'returns.csv', index_col=0)
    index_r = [pd.Timestamp(date) for date in r.index.values]
    return r.reindex(index_r)  # reset the dates of the index to Timestamp


@fixture
def carry_daily():
    cd = pd.read_csv(r_path / 'carry_daily.csv', index_col=0)
    index_cd = [pd.Timestamp(date) for date in cd.index.values]
    return cd.reindex(index_cd)  # reset the dates of the index to Timestamp


@fixture
def return_daily():
    rd = pd.read_csv(r_path / 'return_daily.csv', index_col=0)
    index_rd = [pd.Timestamp(date) for date in rd.index.values]
    return rd.reindex(index_rd)  # reset the dates of the index to Timestamp


def test_format_data(fica_inputs, asset_inputs, all_data, curve):
    returns = f.format_data(fica_inputs, asset_inputs, all_data)
    pd.testing.assert_frame_equal(curve, returns)


def test_calculate_carry_roll_down(fica_inputs, asset_inputs, curve, carry_roll, country_returns):
    returns_carry_roll, returns_country_returns = f.calculate_carry_roll_down(fica_inputs, asset_inputs, curve)

    pd.testing.assert_frame_equal(carry_roll, returns_carry_roll, check_names=False)
    pd.testing.assert_frame_equal(country_returns, returns_country_returns, check_names=False)


def test_calculate_signals_and_returns(fica_inputs, carry_roll, country_returns, signals, cum_contribution, returns):
    return_signals, returns_cum_contribution, returns_returns = f.calculate_signals_and_returns(fica_inputs, carry_roll, country_returns)

    pd.testing.assert_frame_equal(signals, return_signals)
    pd.testing.assert_frame_equal(cum_contribution, returns_cum_contribution)
    pd.testing.assert_frame_equal(returns, returns_returns)


def test_run_daily_attribution(fica_inputs, asset_inputs, all_data, signals, carry_daily, return_daily):
    returns_carry_daily, returns_return_daily = f.run_daily_attribution(fica_inputs, asset_inputs, all_data, signals)

    pd.testing.assert_frame_equal(carry_daily, returns_carry_daily)
    pd.testing.assert_frame_equal(return_daily, returns_return_daily)