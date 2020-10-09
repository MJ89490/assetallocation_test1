from pathlib import Path

import pandas as pd
from pytest import fixture
from psycopg2.extras import DateTimeTZRange

from assetallocation_arp.models import fica as f
from assetallocation_arp.data_etl.dal.data_models.strategy import Fica
from assetallocation_arp.data_etl.dal.data_models.asset import FicaAssetInput, AssetAnalytic
from assetallocation_arp.data_etl.dal.data_models.ticker import Ticker


r_path = Path(__file__).parent / 'resources' / 'fica'


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


@fixture
def fica_strategy(fica_inputs, asset_inputs, all_data):
    f = Fica(fica_inputs['coupon'].iat[0], fica_inputs['curve'].iat[0],
             DateTimeTZRange(fica_inputs['date_from'].iat[0], fica_inputs['date_to'].iat[0]),
             [fica_inputs[f'strategy_weights_{i}'].iat[0] for i in range(1, 11)],
             fica_inputs['tenor'].iat[0] ,fica_inputs['trading_costs'].iat[0])

    f_asset_inputs = []
    for i in asset_inputs.itertuples():
        soverign_ticker = Ticker('sovereign', i.sovereign_ticker_3m, i.sovereign_ticker_1y, i.sovereign_ticker_2y,
                                 i.sovereign_ticker_3y, i.sovereign_ticker_4y, i.sovereign_ticker_5y,
                                 i.sovereign_ticker_6y, i.sovereign_ticker_7y, i.sovereign_ticker_8y,
                                 i.sovereign_ticker_9y, i.sovereign_ticker_10y, i.sovereign_ticker_15y,
                                 i.sovereign_ticker_20y, i.sovereign_ticker_30y)
        swap_ticker = Ticker('swap', i.swap_ticker_3m, i.swap_ticker_1y, i.swap_ticker_2y,
                                 i.swap_ticker_3y, i.swap_ticker_4y, i.swap_ticker_5y,
                                 i.swap_ticker_6y, i.swap_ticker_7y, i.swap_ticker_8y,
                                 i.swap_ticker_9y, i.swap_ticker_10y, i.swap_ticker_15y,
                                 i.swap_ticker_20y, i.swap_ticker_30y)
        swap_cr_ticker = Ticker('swap_cr', i.cr_swap_ticker_3m, i.cr_swap_ticker_1y, '', '', '', '', '', '', '',
                                 i.cr_swap_ticker_9y, i.cr_swap_ticker_10y, '', '', '')
        fa = FicaAssetInput(i.future_ticker, soverign_ticker, swap_ticker, swap_cr_ticker)

        for ticker, data in all_data.items():
            if ticker == fa.ticker:
                for index, val in data.iteritems():
                    fa.add_analytic(AssetAnalytic(ticker, 'PX_LAST', index, float(val)))

        f_asset_inputs.append(fa)

    f.asset_inputs = f_asset_inputs

    return f


def test_format_data(fica_strategy, curve):
    returns = f.format_data(fica_strategy)
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
