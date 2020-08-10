import mock
import pytest
from decimal import Decimal

from assetallocation_arp.data_etl.dal.arp_proc_caller import (ArpProcCaller, Times, TimesAsset, FundStrategy,
                                                              FundStrategyAssetAnalytic, FundStrategyAssetWeight)
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


def test_insert_times_strategy_calls_call_proc(MockTimes, mock_call_proc):
    mock_times = MockTimes(1, 'weekly', 'e', [Decimal(2)], [Decimal(3)], 4, 5)
    user_id = 'a'
    asset_tickers = ['a', 'b']

    a = ArpProcCaller()
    a.insert_times_strategy(mock_times, user_id, asset_tickers)

    mock_call_proc.assert_called_once_with(a, 'arp.insert_times_strategy',
                                           [mock_times.description, 'a', mock_times.time_lag_interval,
                                            mock_times.leverage_type.name, mock_times.volatility_window,
                                            mock_times.short_signals, mock_times.long_signals,
                                            mock_times.frequency.name, mock_times.day_of_week.value, asset_tickers])


def test_insert_times_strategy_returns_t_version(MockTimes, mock_call_proc):
    mock_times = MockTimes(1, 'weekly', 'e', [Decimal(2)], [Decimal(3)], 4, 5)
    expected = 5
    mock_call_proc.return_value = [{'t_version': expected}]

    a = ArpProcCaller()
    returns = a.insert_times_strategy(mock_times, 'a', ['a', 'b'])

    assert expected == returns


def test_select_times_strategy_calls_call_proc(mock_call_proc):
    times_version = 2
    mock_call_proc.return_value = []

    a = ArpProcCaller()
    a.select_times_strategy(times_version)

    mock_call_proc.assert_called_once_with(a, 'arp.select_times_strategy', [times_version])


def test_select_times_strategy_returns_times_object(MockTimes):
    a = ArpProcCaller()

    returns = a.select_times_strategy(2)

    assert isinstance(returns, Times)


def test_select_times_assets_calls_call_proc(mock_call_proc):
    times_version = 2
    business_datetime = datetime(2020, 9, 1)
    mock_call_proc.return_value = []

    a = ArpProcCaller()
    a.select_times_assets(times_version, business_datetime)

    mock_call_proc.assert_called_once_with(a, 'arp.select_times_assets', [times_version, business_datetime])


def test_select_times_assets_returns_list_of_times_asset_objects(mock_call_proc):
    times_version = 2
    business_datetime = datetime(2020, 9, 1)
    mock_call_proc.return_value = [mock.MagicMock(), mock.MagicMock(), mock.MagicMock()]

    with mock.patch('assetallocation_arp.data_etl.dal.arp_proc_caller.TimesAsset', autospec=True):
        a = ArpProcCaller()
        returns = a.select_times_assets(times_version, business_datetime)

    assert isinstance(returns, list)
    assert all([isinstance(i, TimesAsset) for i in returns])


@mock.patch('assetallocation_arp.data_etl.dal.arp_proc_caller.FundStrategy', autospec=True)
def test_insert_fund_strategy_results_calls_call_proc(MockFundStrategy, mock_call_proc):
    user_id = 'a'
    fund_strategy = MockFundStrategy('a', 'times', 1, 2)

    a = ArpProcCaller()
    a.insert_fund_strategy_results(fund_strategy, user_id)

    mock_call_proc.assert_called_once_with(a, 'arp.insert_fund_strategy_results',
                                          [fund_strategy.business_datetime, fund_strategy.fund_name,
                                           fund_strategy.output_is_saved, fund_strategy.strategy_name.name,
                                           fund_strategy.strategy_version, fund_strategy.weight, user_id,
                                           fund_strategy.python_code_version, [], []])


@mock.patch('assetallocation_arp.data_etl.dal.arp_proc_caller.FundStrategy', autospec=True)
def test_insert_fund_strategy_results_returns_true_when_fund_strategy_id_is_not_none(MockFundStrategy, mock_call_proc):
    user_id = 'a'
    fund_strategy = MockFundStrategy('a', 'times', 1, 2)
    mock_call_proc.return_value = [{'fund_strategy_id': 4}]

    a = ArpProcCaller()
    returns = a.insert_fund_strategy_results(fund_strategy, user_id)

    assert returns is True


@mock.patch('assetallocation_arp.data_etl.dal.arp_proc_caller.FundStrategy', autospec=True)
def test_insert_fund_strategy_results_returns_false_when_fund_strategy_id_is_none(MockFundStrategy, mock_call_proc):
    user_id = 'a'
    fund_strategy = MockFundStrategy('a', 'times', 1, 2)
    mock_call_proc.return_value = [{'fund_strategy_id': None}]

    a = ArpProcCaller()
    returns = a.insert_fund_strategy_results(fund_strategy, user_id)

    assert returns is False


def test_analytics_to_composite_returns_expected_value():
    mock_fsaa1 = mock_fund_strategy_asset_analytic('a', 'b', 'c', 1)
    mock_fsaa2 = mock_fund_strategy_asset_analytic('d', 'e', 'f', 2)

    returns = ArpProcCaller._analytics_to_composite([mock_fsaa1, mock_fsaa2])

    expected = ['("a","b","c",1)', '("d","e","f",2)']
    assert expected == returns


def mock_fund_strategy_asset_analytic(asset_ticker: str, category: str, subcategory: str, value: Decimal):
    MockFundStrategyAssetAnalytic = mock.create_autospec(FundStrategyAssetAnalytic)
    mock_fsaa = MockFundStrategyAssetAnalytic(asset_ticker, category, subcategory, value)
    mock_fsaa.asset_ticker = asset_ticker
    mock_fsaa.category = category
    mock_fsaa.subcategory = subcategory
    mock_fsaa.value = value
    return mock_fsaa


def test_weight_to_composite_returns_expected_value():
    mock_fsaa1 = mock_fund_strategy_asset_weights('a', Decimal(1), Decimal(2))
    mock_fsaa2 = mock_fund_strategy_asset_weights('c', Decimal(4), Decimal(3))

    returns = ArpProcCaller._weights_to_composite([mock_fsaa1, mock_fsaa2])

    expected = ['("a",1,2)', '("c",4,3)']
    assert expected == returns


def mock_fund_strategy_asset_weights(asset_ticker: str, strategy_weight: Decimal, implemented_weight: Decimal):
    MockFundStrategyAssetWeight = mock.create_autospec(FundStrategyAssetWeight)
    mock_fsaw = MockFundStrategyAssetWeight(asset_ticker, strategy_weight)
    mock_fsaw.asset_ticker = asset_ticker
    mock_fsaw.strategy_weight = strategy_weight
    mock_fsaw.implemented_weight = implemented_weight
    return mock_fsaw


def test_select_fund_strategy_results_calls_call_proc(mock_call_proc):
    fund_name = 'b'
    strategy_name = 'times'
    business_datetime = datetime(2020, 2, 1)
    system_datetime = datetime(2021, 3, 4)
    mock_call_proc.return_value = []

    a = ArpProcCaller()
    a.select_fund_strategy_results(fund_name, strategy_name, business_datetime, system_datetime)

    mock_call_proc.assert_called_once_with(a, 'arp.select_fund_strategy_results',
                                           [fund_name, strategy_name, business_datetime, system_datetime])


def test_select_times_assets_returns_fund_strategy(mock_call_proc):
    fund_name = 'b'
    strategy_name = 'times'
    business_datetime = datetime(2020, 2, 1)
    system_datetime = datetime(2021, 3, 4)
    mock_call_proc.return_value = [mock.MagicMock(), mock.MagicMock(), mock.MagicMock()]

    with mock.patch('assetallocation_arp.data_etl.dal.arp_proc_caller.FundStrategy', autospec=True):
        a = ArpProcCaller()
        returns = a.select_fund_strategy_results(fund_name, strategy_name, business_datetime, system_datetime)

    assert isinstance(returns, FundStrategy)
