from pathlib import Path

from pytest import fixture
from psycopg2.extras import DateTimeTZRange

from assetallocation_arp.models import maven
from tests.assetallocation_arp.models.resources.helper import read_inputs_outputs, assert_equal
from assetallocation_arp.data_etl.dal.data_models.strategy import Maven
from assetallocation_arp.data_etl.dal.data_models.asset import MavenAssetInput
from assetallocation_arp.data_etl.dal.data_models.asset_analytic import AssetAnalytic
from assetallocation_arp.common_libraries.dal_enums.strategy import DayOfWeek

resource_path = Path(__file__).parent / 'resources' / 'maven'


@fixture
def maven_strategy():
    def make_maven_strategy(maven_inputs, asset_inputs, all_data):
        # the database will filter the data between the dates below

        m = Maven(
            maven_inputs['er_tr'].iat[0],
            maven_inputs['frequency'].iat[0],
            DayOfWeek[maven_inputs['week_day'].iat[0]],
            DateTimeTZRange(maven_inputs['date_from'].iat[0], maven_inputs['date_to'].iat[0]),
            maven_inputs['number_assets'].iat[0],
            maven_inputs['long_cutoff'].iat[0],
            maven_inputs['short_cutoff'].iat[0],
            maven_inputs['val_period_months'].iat[0],
            maven_inputs['val_period_base'].iat[0],
            [maven_inputs[f'momentum_weight_{i}m'].iat[0] for i in range(1, 7)],
            [maven_inputs[f'volatility_weight_{i}y'].iat[0] for i in range(1, 6)]
        )

        if asset_inputs is not None:
            data = all_data.loc[maven_inputs['date_from'].iat[0]:maven_inputs['date_to'].iat[0]]
            maven_asset_inputs = []
            for r, asset in asset_inputs.iterrows():
                mai = MavenAssetInput(
                    asset.loc['asset'],
                    asset.loc['description'],
                    asset.loc['bbg_tr_ticker'],
                    asset.loc['bbg_er_ticker'],
                    asset.loc['currency'],
                    asset.loc['cash_ticker'],
                    asset.loc['asset_class'],
                    asset.loc['true_excess'],
                    asset.loc['asset_weight'],
                    asset.loc['transaction_costs']
                )

                mai.bbg_tr_asset.asset_analytics = [
                    AssetAnalytic(mai.bbg_tr_ticker, 'PX_LAST', index, float(val)) for index, val
                    in data.loc[:, mai.bbg_tr_ticker].iteritems()
                ]
                mai.bbg_er_asset.asset_analytics = [
                    AssetAnalytic(mai.bbg_er_ticker, 'PX_LAST', index, float(val)) for index, val
                    in data.loc[:, mai.bbg_er_ticker].iteritems()
                ]

                maven_asset_inputs.append(mai)

            m.asset_inputs = maven_asset_inputs

        return m
    return make_maven_strategy


def test_format_data(maven_strategy):
    test_kwargs, expected = read_inputs_outputs(resource_path / 'format_data')
    m = maven_strategy(test_kwargs.pop('maven_inputs'), test_kwargs.pop('asset_inputs'), test_kwargs.pop('all_data'))
    returns = maven.format_data(m, **test_kwargs)

    if isinstance(returns, tuple):
        for counter, v in enumerate(returns):
            assert_equal(str(counter), expected, v)

    else:
        assert_equal('0', expected, returns)


def test_calculate_excess_returns(maven_strategy):
    test_kwargs, expected = read_inputs_outputs(resource_path / 'calculate_excess_returns')
    m = maven_strategy(test_kwargs.pop('maven_inputs'), test_kwargs.pop('asset_inputs'), test_kwargs.pop('all_data'))
    returns = maven.calculate_excess_returns(m, **test_kwargs)

    if isinstance(returns, tuple):
        for counter, v in enumerate(returns):
            assert_equal(str(counter), expected, v)

    else:
        assert_equal('0', expected, returns)


def test_calculate_signals(maven_strategy):
    test_kwargs, expected = read_inputs_outputs(resource_path / 'calculate_signals')
    m = maven_strategy(test_kwargs.pop('maven_inputs'), None, None)
    returns = maven.calculate_signals(m, **test_kwargs)

    if isinstance(returns, tuple):
        for counter, v in enumerate(returns):
            assert_equal(str(counter), expected, v)

    else:
        assert_equal('0', expected, returns)


def test_run_performance_stats_old():
    test_kwargs, expected = read_inputs_outputs(resource_path / 'run_performance_stats')
    del test_kwargs['all_data']
    returns = maven.run_performance_stats_old(**test_kwargs)

    if isinstance(returns, tuple):
        for counter, v in enumerate(returns):
            assert_equal(str(counter), expected, v)

    else:
        assert_equal('0', expected, returns)


def test_run_performance_stats(maven_strategy):
    test_kwargs, expected = read_inputs_outputs(resource_path / 'run_performance_stats')
    m = maven_strategy(test_kwargs.pop('maven_inputs'), test_kwargs.pop('asset_inputs'), test_kwargs.pop('all_data'))
    returns = maven.run_performance_stats(m, **test_kwargs)

    if isinstance(returns, tuple):
        for counter, v in enumerate(returns):
            assert_equal(str(counter), expected, v)

    else:
        assert_equal('0', expected, returns)

