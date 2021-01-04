from pathlib import Path

import pandas as pd
from pytest import fixture
from psycopg2.extras import DateTimeTZRange

from assetallocation_arp.models import fica as f
from assetallocation_arp.data_etl.dal.data_models.strategy import Fica
from assetallocation_arp.data_etl.dal.data_models.asset import FicaAssetInput, AssetAnalytic, FicaAssetInputGroup
from assetallocation_arp.common_libraries.dal_enums.fica_asset_input import CurveTenor, CurveName


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
def fica_strategy(fica_inputs, asset_inputs, all_data) -> Fica:
    # the database will filter the data between the dates below
    data = all_data.loc[fica_inputs['date_from'].iat[0]:fica_inputs['date_to'].iat[0]]

    f = Fica(fica_inputs['coupon'].iat[0], fica_inputs['curve'].iat[0],
             DateTimeTZRange(fica_inputs['date_from'].iat[0], fica_inputs['date_to'].iat[0]),
             [fica_inputs[f'strategy_weights_{i}'].iat[0] for i in range(1, 11)],
             fica_inputs['tenor'].iat[0], fica_inputs['trading_costs'].iat[0])

    tickers = {'3m': CurveTenor.mth3, '1y': CurveTenor.yr1, '2y': CurveTenor.yr2, '3y': CurveTenor.yr3,
               '4y': CurveTenor.yr4, '5y': CurveTenor.yr5, '6y': CurveTenor.yr6, '7y': CurveTenor.yr7,
               '8y': CurveTenor.yr8, '9y': CurveTenor.yr9, '10y': CurveTenor.yr10, '15y': CurveTenor.yr15,
               '20y': CurveTenor.yr20, '30y': CurveTenor.yr30}

    cr_tickers = {'3m': CurveTenor.mth3, '1y': CurveTenor.yr1, '9y': CurveTenor.yr9, '10y': CurveTenor.yr10}

    grouped_asset_inputs = []
    for r, asset in asset_inputs.iterrows():
        asset_input_group = []
        for i, j in tickers.items():
            so_ticker = asset.loc[f'sovereign_ticker_{i}']
            so_fai = FicaAssetInput(so_ticker, CurveName.sovereign, j)
            so_fai.country = asset.loc['country']
            so_fai.asset_analytics = [AssetAnalytic(so_ticker, 'PX_LAST', index, float(val)) for index, val
                                      in data.loc[:, so_ticker].iteritems() if pd.notna(val)]
            asset_input_group.append(so_fai)

            sw_ticker = asset.loc[f'swap_ticker_{i}']
            sw_fai = FicaAssetInput(sw_ticker, CurveName.swap, j)
            sw_fai.country = asset.loc['country']
            sw_fai.asset_analytics = [AssetAnalytic(sw_ticker, 'PX_LAST', index, float(val)) for index, val in
                                      data.loc[:, sw_ticker].iteritems() if pd.notna(val)]
            asset_input_group.append(sw_fai)

            if i in cr_tickers:
                cr_ticker = asset.loc[f'cr_swap_ticker_{i}']
                cr_fai = FicaAssetInput(cr_ticker, CurveName.swap_cr, j)
                cr_fai.country = asset.loc['country']
                cr_fai.asset_analytics = [AssetAnalytic(cr_ticker, 'PX_LAST', index, float(val)) for index, val in
                                          data.loc[:, cr_ticker].iteritems() if pd.notna(val)]
                asset_input_group.append(cr_fai)

        future_ticker = asset.loc['future_ticker']
        if pd.notna(future_ticker):
            future_asset_input = FicaAssetInput(future_ticker, CurveName.future, None)
            future_asset_input.country = asset.loc['country']
            future_asset_input.asset_analytics = [AssetAnalytic(future_ticker, 'PX_LAST', index, float(val)) for index, val
                                                  in data.loc[:, future_ticker].iteritems() if pd.notna(val)]
            asset_input_group.append(future_asset_input)

        grouped_asset_inputs.append(FicaAssetInputGroup(asset.loc['country'], asset_input_group))

    f.grouped_asset_inputs = grouped_asset_inputs

    return f


def test_format_data(fica_strategy, curve):
    returns = f.format_data(fica_strategy)
    pd.testing.assert_frame_equal(curve, returns, check_names=False, check_like=True)


def test_calculate_carry_roll_down(fica_strategy, curve, carry_roll, country_returns):
    returns_carry_roll, returns_country_returns = f.calculate_carry_roll_down(fica_strategy, curve)

    pd.testing.assert_frame_equal(carry_roll, returns_carry_roll, check_names=False, check_like=True)
    pd.testing.assert_frame_equal(country_returns, returns_country_returns, check_names=False, check_like=True)


def test_calculate_signals_and_returns(fica_strategy, carry_roll, country_returns, signals, cum_contribution, returns):
    return_signals, returns_cum_contribution, returns_returns = f.calculate_signals_and_returns(fica_strategy, carry_roll, country_returns)

    pd.testing.assert_frame_equal(signals, return_signals)
    pd.testing.assert_frame_equal(cum_contribution, returns_cum_contribution)
    pd.testing.assert_frame_equal(returns, returns_returns)


def test_run_daily_attribution(fica_strategy, signals, carry_daily, return_daily):
    returns_carry_daily, returns_return_daily = f.run_daily_attribution(fica_strategy, signals)

    pd.testing.assert_frame_equal(carry_daily, returns_carry_daily, check_names=False)
    pd.testing.assert_frame_equal(return_daily, returns_return_daily, check_names=False)

