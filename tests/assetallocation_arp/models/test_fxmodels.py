from pathlib import Path

from pytest import fixture
from psycopg2.extras import DateTimeTZRange

from assetallocation_arp.models import fxmodels as fx
from tests.assetallocation_arp.models.resources.helper import read_inputs_outputs, assert_equal
from assetallocation_arp.data_etl.dal.data_models.strategy import Fx
from assetallocation_arp.data_etl.dal.data_models.asset import FxAssetInput, Asset, AssetAnalytic

resource_path = Path(__file__).parent / 'resources' / 'fxmodels'


@fixture
def fx_strategy():
    def make_fx_strategy(fxmodels_inputs, asset_inputs, all_data):
        # the database will filter the data between the dates below

        f = Fx(
            fxmodels_inputs['model'].iat[0].lower(),
            fxmodels_inputs['signal'].iat[0],
            fxmodels_inputs['currency'].iat[0],
            fxmodels_inputs['response function'].iat[0],
            fxmodels_inputs['exposure'].iat[0],
            [fxmodels_inputs[f'momentum_weight_{i}m'].iat[0] for i in range(1, 7)],
            fxmodels_inputs['transaction costs'].iat[0]
        )

        f.top_crosses = fxmodels_inputs['top crosses'].iat[0]
        f.vol_window = fxmodels_inputs['vol window'].iat[0]
        f.value_window = fxmodels_inputs['value window'].iat[0]
        f.sharpe_cutoff = fxmodels_inputs['sharpe cutoff'].iat[0]
        f.sharpe_cutoff = fxmodels_inputs['sharpe cutoff'].iat[0]
        f.historical_base = fxmodels_inputs['historical base'].iat[0]
        f.mean_reversion = fxmodels_inputs['mean reversion'].iat[0]
        f.defensive = True

        if asset_inputs is not None:
            data = all_data.loc[fxmodels_inputs['date_from'].iat[0]:fxmodels_inputs['date_to'].iat[0]]
            fx_asset_inputs = []
            for r, asset in asset_inputs.iterrows():
                ppp_ticker = asset.loc['ppp']
                cash_rate_ticker = asset.loc['cash_rate']

                fai = FxAssetInput(ppp_ticker, cash_rate_ticker, asset.loc['currency'])
                fai.ppp_asset = Asset(ppp_ticker)
                fai.ppp_asset.asset_analytics = [
                    AssetAnalytic(ppp_ticker, 'PX_LAST', index, float(val)) for index, val
                    in data.loc[:, ppp_ticker].iteritems()
                ]

                fai.cash_rate_asset = Asset(cash_rate_ticker)
                fai.cash_rate_asset.asset_analytics = [
                    AssetAnalytic(cash_rate_ticker, 'PX_LAST', index, float(val)) for index, val in
                    data.loc[:, cash_rate_ticker].iteritems()
                ]

                fx_asset_inputs.append(fai)

            f.asset_inputs = fx_asset_inputs

            carry_tickers = FxAssetInput.get_carry_tickers(f.asset_inputs)
            f.carry_assets = [Asset(ticker) for ticker in carry_tickers]
            for i in f.carry_assets:
                i.asset_analytics = [AssetAnalytic(i.ticker, 'PX_LAST', index, float(val)) for index, val in
                    data.loc[:, i.ticker].iteritems()]

            spot_tickers = FxAssetInput.get_spot_tickers(f.asset_inputs)
            f.spot_assets = [Asset(ticker) for ticker in spot_tickers]
            for i in f.spot_assets:
                i.asset_analytics = [
                    AssetAnalytic(i.ticker, 'PX_LAST', index, float(val)) for index, val in
                    data.loc[:, i.ticker].iteritems()
                ]

        return f
    return make_fx_strategy


def test_create_sizing_mapping():
    test_kwargs, expected = read_inputs_outputs(resource_path / 'create_sizing_map')

    returns = fx.create_sizing_mapping(**test_kwargs)

    if isinstance(returns, tuple):
        for counter, v in enumerate(returns):
            assert_equal(str(counter), expected, v)

    else:
        assert_equal('0', expected, returns)


def test_format_data(fx_strategy):
    test_kwargs, expected = read_inputs_outputs(resource_path / 'format_data')
    f = fx_strategy(test_kwargs.pop('fxmodels_inputs'), test_kwargs.pop('asset_inputs'), test_kwargs.pop('all_data'))
    returns = fx.format_data(f, **test_kwargs)

    if isinstance(returns, tuple):
        for counter, v in enumerate(returns):
            assert_equal(str(counter), expected, v)

    else:
        assert_equal('0', expected, returns)


def test_calculate_signals(fx_strategy):
    test_kwargs, expected = read_inputs_outputs(resource_path / 'calculate_signals')
    f = fx_strategy(test_kwargs.pop('fxmodels_inputs'), test_kwargs.pop('asset_inputs'), test_kwargs.pop('all_data'))
    returns = fx.calculate_signals(f, **test_kwargs)

    if isinstance(returns, tuple):
        for counter, v in enumerate(returns):
            assert_equal(str(counter), expected, v)

    else:
        assert_equal('0', expected, returns)


def test_determine_sizing(fx_strategy):
    test_kwargs, expected = read_inputs_outputs(resource_path / 'determine_sizing')
    f = fx_strategy(test_kwargs.pop('fxmodels_inputs'), test_kwargs.pop('asset_inputs'), test_kwargs.pop('all_data'))
    returns = fx.determine_sizing(f, **test_kwargs)

    if isinstance(returns, tuple):
        for counter, v in enumerate(returns):
            assert_equal(str(counter), expected, v)

    else:
        assert_equal('0', expected, returns)


def test_calculate_returns(fx_strategy):
    test_kwargs, expected = read_inputs_outputs(resource_path / 'calculate_returns')
    f = fx_strategy(test_kwargs.pop('fxmodels_inputs'), None, None)
    returns = fx.calculate_returns(f, **test_kwargs)

    if isinstance(returns, tuple):
        for counter, v in enumerate(returns):
            assert_equal(str(counter), expected, v)

    else:
        assert_equal('0', expected, returns)
