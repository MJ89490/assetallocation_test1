import mock
import pytest

from psycopg2.extras import DateTimeTZRange

from assetallocation_arp.data_etl.dal.arp_proc_caller import TimesProcCaller, Times, TimesAssetInput, FundStrategy, \
    EffectProcCaller, Effect, ArpProcCaller, EffectAssetInput, FicaProcCaller, Fica, FicaAssetInput
from datetime import datetime


@pytest.fixture(autouse=True)
def mock_engine():
    with mock.patch('assetallocation_arp.data_etl.dal.db.create_engine') as _mock_engine:
        yield _mock_engine


@pytest.fixture(autouse=True)
def mock_call_proc():
    with mock.patch.object(ArpProcCaller, 'call_proc', autospec=True) as _mock_call_proc:
        yield _mock_call_proc


@pytest.fixture()
def MockTimes():
    with mock.patch('assetallocation_arp.data_etl.dal.arp_proc_caller.Times', autospec=True) as _MockTimes:
        yield _MockTimes


@pytest.fixture()
def MockEffect():
    with mock.patch('assetallocation_arp.data_etl.dal.arp_proc_caller.Effect', autospec=True) as _MockEffect:
        yield _MockEffect


@pytest.fixture()
def MockFica():
    with mock.patch('assetallocation_arp.data_etl.dal.arp_proc_caller.Fica', autospec=True) as _MockFica:
        yield _MockFica


@pytest.fixture()
def MockFicaAssetInput():
    with mock.patch('assetallocation_arp.data_etl.dal.arp_proc_caller.FicaAssetInput', autospec=True) as _MockFicaAssetInput:
        yield _MockFicaAssetInput


@pytest.fixture()
def MockAsset():
    with mock.patch('assetallocation_arp.data_etl.dal.arp_proc_caller.Asset', autospec=True) as _MockAsset:
        yield _MockAsset


def test_insert_times_strategy_calls_call_proc(MockTimes, mock_call_proc):
    mock_times = MockTimes(1, 'weekly', 'e', [float(2)], [float(3)], 4, 5)
    user_id = 'a'

    a = TimesProcCaller()
    a._insert_times_strategy(mock_times, user_id)

    mock_call_proc.assert_called_once_with(a, 'arp.insert_times_strategy',
                                           [mock_times.description, 'a', mock_times.time_lag_interval,
                                            mock_times.leverage_type.name, mock_times.volatility_window,
                                            mock_times.short_signals, mock_times.long_signals,
                                            mock_times.frequency.name, mock_times.day_of_week.value])


def test_insert_times_strategy_returns_t_version(MockTimes, mock_call_proc):
    mock_times = MockTimes(1, 'weekly', 'e', [float(2)], [float(3)], 4, 5)
    expected = 5
    mock_call_proc.return_value = [{'t_version': expected}]

    a = TimesProcCaller()
    returns = a._insert_times_strategy(mock_times, 'a')

    assert expected == returns


def test_select_times_strategy_calls_call_proc(mock_call_proc):
    times_version = 2
    mock_call_proc.return_value = []

    a = TimesProcCaller()
    a._select_times_strategy(times_version)

    mock_call_proc.assert_called_once_with(a, 'arp.select_times_strategy', [times_version])


def test_select_times_strategy_returns_times_object(MockTimes):
    a = TimesProcCaller()

    returns = a._select_times_strategy(2)

    assert isinstance(returns, Times)


def test_select_times_assets_with_analytics_calls_call_proc(mock_call_proc):
    times_version = 2
    business_datetime = datetime(2020, 9, 1)
    mock_call_proc.return_value = []

    a = TimesProcCaller()
    a.select_times_assets_with_analytics(times_version, business_datetime)

    mock_call_proc.assert_called_once_with(a, 'arp.select_times_assets_with_analytics', [times_version, business_datetime])


def test_select_times_assets_returns_list_of_times_asset_objects(mock_call_proc):
    times_version = 2
    business_datetime = datetime(2020, 9, 1)
    mock_call_proc.return_value = [mock.MagicMock(), mock.MagicMock(), mock.MagicMock()]

    with mock.patch('assetallocation_arp.data_etl.dal.arp_proc_caller.TimesAssetInput', autospec=True):
        a = TimesProcCaller()
        returns = a.select_times_assets_with_analytics(times_version, business_datetime)

    assert isinstance(returns, list)
    assert all([isinstance(i, TimesAssetInput) for i in returns])


@mock.patch('assetallocation_arp.data_etl.dal.arp_proc_caller.FundStrategy', autospec=True)
def test_insert_fund_strategy_results_calls_call_proc(MockFundStrategy, mock_call_proc):
    user_id = 'a'
    fund_strategy = MockFundStrategy('a', 'times', 1, 2)

    a = TimesProcCaller()
    a.insert_fund_strategy_results(fund_strategy, user_id)

    mock_call_proc.assert_called_once_with(a, 'arp.insert_fund_strategy_results',
                                          [fund_strategy.fund_name,
                                           fund_strategy.output_is_saved, fund_strategy.strategy_name.name,
                                           fund_strategy.strategy_version, fund_strategy.weight, user_id,
                                           fund_strategy.python_code_version, [], []])


@mock.patch('assetallocation_arp.data_etl.dal.arp_proc_caller.FundStrategy', autospec=True)
def test_insert_fund_strategy_results_returns_true_when_fund_strategy_id_is_not_none(MockFundStrategy, mock_call_proc):
    user_id = 'a'
    fund_strategy = MockFundStrategy('a', 'times', 1, 2)
    mock_call_proc.return_value = [{'fund_strategy_id': 4}]

    a = TimesProcCaller()
    returns = a.insert_fund_strategy_results(fund_strategy, user_id)

    assert returns is True


@mock.patch('assetallocation_arp.data_etl.dal.arp_proc_caller.FundStrategy', autospec=True)
def test_insert_fund_strategy_results_returns_false_when_res_is_empty(MockFundStrategy, mock_call_proc):
    user_id = 'a'
    fund_strategy = MockFundStrategy('a', 'times', 1, 2)
    mock_call_proc.return_value = [{}]

    a = TimesProcCaller()
    returns = a.insert_fund_strategy_results(fund_strategy, user_id)

    assert returns is False


def test_select_fund_strategy_results_calls_call_proc(mock_call_proc):
    fund_name = 'b'
    strategy_name = 'times'
    strategy_version = 2
    mock_call_proc.return_value = []

    a = TimesProcCaller()
    a.select_fund_strategy_results(fund_name, strategy_name, strategy_version)

    mock_call_proc.assert_called_once_with(a, 'arp.select_fund_strategy_results',
                                           [fund_name, strategy_name, strategy_version])


def test_select_fund_strategy_results_returns_fund_strategy(mock_call_proc, MockAsset):
    fund_name = 'b'
    strategy_name = 'times'
    strategy_version = 1
    mock_call_proc.return_value = [mock.MagicMock(), mock.MagicMock(), mock.MagicMock()]

    with mock.patch('assetallocation_arp.data_etl.dal.arp_proc_caller.FundStrategy', autospec=True):
        a = TimesProcCaller()
        returns = a.select_fund_strategy_results(fund_name, strategy_name, strategy_version)

    assert isinstance(returns, FundStrategy)


def test_insert_effect_strategy_calls_call_proc(MockEffect, mock_call_proc):
    mock_effect = MockEffect('Nominal', 1, 1, 1, 'monthly', 1, 1, 1, 1, 1, 1, 1, 'TotalReturn')
    user_id = 'a'

    a = EffectProcCaller()
    a._insert_effect_strategy(mock_effect, user_id)

    mock_call_proc.assert_called_once_with(a, 'arp.insert_effect_strategy',
                                           [mock_effect.description, 'a', mock_effect.carry_type.name,
                                            mock_effect.closing_threshold, mock_effect.cost,
                                            mock_effect.day_of_week.value, mock_effect.frequency.name,
                                            mock_effect.include_shorts, mock_effect.inflation_lag_interval,
                                            mock_effect.interest_rate_cut_off_long,
                                            mock_effect.interest_rate_cut_off_short,
                                            mock_effect.moving_average_long_term, mock_effect.moving_average_short_term,
                                            mock_effect.is_realtime_inflation_forecast, mock_effect.trend_indicator.name
                                            ])


def test_insert_effect_strategy_returns_e_version(MockEffect, mock_call_proc):
    mock_effect = MockEffect('Nominal', 1, 1, 1, 'monthly', 1, 1, 1, 1, 1, 1, 1, 'TotalReturn')
    expected = 5
    mock_call_proc.return_value = [{'e_version': expected}]

    a = EffectProcCaller()
    returns = a._insert_effect_strategy(mock_effect, 'a')

    assert expected == returns


def test_select_effect_strategy_calls_call_proc(mock_call_proc):
    e_version = 2
    mock_call_proc.return_value = []

    a = EffectProcCaller()
    a._select_effect_strategy(e_version)

    mock_call_proc.assert_called_once_with(a, 'arp.select_effect_strategy', [e_version])


def test_select_effect_strategy_returns_effect_object(MockEffect):
    a = EffectProcCaller()

    returns = a._select_effect_strategy(2)

    assert isinstance(returns, Effect)


def test_select_effect_assets_with_analytics_calls_call_proc(mock_call_proc):
    e_version = 2
    business_datetime = datetime(2020, 9, 1)
    mock_call_proc.return_value = []

    a = EffectProcCaller()
    a.select_effect_assets_with_analytics(e_version, business_datetime)

    mock_call_proc.assert_called_once_with(a, 'arp.select_effect_assets_with_analytics', [e_version, business_datetime])


def test_select_effect_assets_returns_list_of_effect_asset_objects(mock_call_proc):
    e_version = 2
    business_datetime = datetime(2020, 9, 1)
    mock_call_proc.return_value = [mock.MagicMock(), mock.MagicMock(), mock.MagicMock()]

    with mock.patch('assetallocation_arp.data_etl.dal.arp_proc_caller.EffectAssetInput', autospec=True):
        a = EffectProcCaller()
        returns = a.select_effect_assets_with_analytics(e_version, business_datetime)

    assert isinstance(returns, list)
    assert all([isinstance(i, EffectAssetInput) for i in returns])


def test_insert_fica_strategy_calls_call_proc(MockFica, mock_call_proc):
    mock_fica = MockFica(1.0, 'curve', DateTimeTZRange(), [1, 1], 1, 1)
    user_id = 'a'

    a = FicaProcCaller()
    a._insert_fica_strategy(mock_fica, user_id)

    mock_call_proc.assert_called_once_with(a, 'arp.insert_fica_strategy',
                                           [mock_fica.description, 'a', mock_fica.coupon,
                                            mock_fica.curve, mock_fica.business_tstzrange,
                                            mock_fica.strategy_weights, mock_fica.tenor,
                                            mock_fica.trading_cost])


def test_insert_fica_strategy_returns_f_version(MockFica, mock_call_proc):
    mock_fica = MockFica(1.0, 'curve', DateTimeTZRange(), [1, 1], 1, 1)
    expected = 5
    mock_call_proc.return_value = [{'f_version': expected}]

    a = FicaProcCaller()
    returns = a._insert_fica_strategy(mock_fica, 'a')

    assert expected == returns


def test_insert_fica_assets_calls_call_proc(MockFicaAssetInput, mock_call_proc):
    mock_fai = MockFicaAssetInput('asd', 'future', None)
    fica_version = 20

    a = FicaProcCaller()
    a._insert_fica_assets(fica_version, [[mock_fai]])

    mock_call_proc.assert_called_once_with(
        a, 'arp.insert_fica_assets', [
            fica_version, [mock_fai.ticker], [mock_fai.category], [mock_fai.curve_tenor]])


def test_select_fica_strategy_calls_call_proc(mock_call_proc):
    f_version = 2
    mock_call_proc.return_value = []

    a = FicaProcCaller()
    a._select_fica_strategy(f_version)

    mock_call_proc.assert_called_once_with(a, 'arp.select_fica_strategy', [f_version])


def test_select_fica_strategy_returns_fica_object(MockFica):
    a = FicaProcCaller()

    returns = a._select_fica_strategy(2)

    assert isinstance(returns, Fica)


def test_select_fica_assets_with_analytics_calls_call_proc(mock_call_proc):
    f_version = 2
    business_datetime = datetime(2020, 9, 1)
    mock_call_proc.return_value = []

    a = FicaProcCaller()
    a.select_fica_assets_with_analytics(f_version, business_datetime)

    mock_call_proc.assert_called_once_with(a, 'arp.select_fica_assets_with_analytics', [f_version, business_datetime])


def test_select_fica_assets_with_analytics_returns_list_of_fica_asset_objects(mock_call_proc):
    f_version = 2
    business_datetime = datetime(2020, 9, 1)
    mock_call_proc.return_value = [mock.MagicMock(), mock.MagicMock(), mock.MagicMock()]

    with mock.patch('assetallocation_arp.data_etl.dal.arp_proc_caller.FicaAssetInput', autospec=True):
        with mock.patch('assetallocation_arp.data_etl.dal.arp_proc_caller.ArpTypeConverter', autospec=True):
            a = FicaProcCaller()
            returns = a.select_fica_assets_with_analytics(f_version, business_datetime)

    assert isinstance(returns, list)
    assert all([isinstance(i, FicaAssetInput) for i in returns])


def test_select_fica_assets_calls_call_proc(mock_call_proc):
    f_version = 2
    mock_call_proc.return_value = []

    a = FicaProcCaller()
    a._select_fica_assets(f_version)

    mock_call_proc.assert_called_once_with(a, 'arp.select_fica_assets', [f_version])


def test_select_fica_assets_returns_list_of_fica_asset_objects(mock_call_proc):
    f_version = 2
    mock_call_proc.return_value = [mock.MagicMock(), mock.MagicMock(), mock.MagicMock()]

    with mock.patch('assetallocation_arp.data_etl.dal.arp_proc_caller.FicaAssetInput', autospec=True):
        a = FicaProcCaller()
        returns = a._select_fica_assets(f_version)

    assert isinstance(returns, list)
    assert all([isinstance(i, FicaAssetInput) for i in returns])
