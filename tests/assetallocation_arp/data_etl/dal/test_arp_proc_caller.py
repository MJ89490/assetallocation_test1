import mock
import pytest

from assetallocation_arp.data_etl.dal.arp_proc_caller import ArpProcCaller, Times, TimesAssetInput, FundStrategy
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
    mock_times = MockTimes(1, 'weekly', 'e', [float(2)], [float(3)], 4, 5)
    user_id = 'a'

    a = ArpProcCaller()
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

    a = ArpProcCaller()
    returns = a._insert_times_strategy(mock_times, 'a')

    assert expected == returns


def test_select_times_strategy_calls_call_proc(mock_call_proc):
    times_version = 2
    mock_call_proc.return_value = []

    a = ArpProcCaller()
    a._select_times_strategy(times_version)

    mock_call_proc.assert_called_once_with(a, 'arp.select_times_strategy', [times_version])


def test_select_times_strategy_returns_times_object(MockTimes):
    a = ArpProcCaller()

    returns = a._select_times_strategy(2)

    assert isinstance(returns, Times)


def test_select_times_assets_with_analytics_calls_call_proc(mock_call_proc):
    times_version = 2
    business_datetime = datetime(2020, 9, 1)
    mock_call_proc.return_value = []

    a = ArpProcCaller()
    a.select_times_assets_with_analytics(times_version, business_datetime)

    mock_call_proc.assert_called_once_with(a, 'arp.select_times_assets_with_analytics', [times_version, business_datetime])


def test_select_times_assets_returns_list_of_times_asset_objects(mock_call_proc):
    times_version = 2
    business_datetime = datetime(2020, 9, 1)
    mock_call_proc.return_value = [mock.MagicMock(), mock.MagicMock(), mock.MagicMock()]

    with mock.patch('assetallocation_arp.data_etl.dal.arp_proc_caller.TimesAssetInput', autospec=True):
        a = ArpProcCaller()
        returns = a.select_times_assets_with_analytics(times_version, business_datetime)

    assert isinstance(returns, list)
    assert all([isinstance(i, TimesAssetInput) for i in returns])


@mock.patch('assetallocation_arp.data_etl.dal.arp_proc_caller.FundStrategy', autospec=True)
def test_insert_fund_strategy_results_calls_call_proc(MockFundStrategy, mock_call_proc):
    user_id = 'a'
    fund_strategy = MockFundStrategy('a', 'times', 1, 2)

    a = ArpProcCaller()
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

    a = ArpProcCaller()
    returns = a.insert_fund_strategy_results(fund_strategy, user_id)

    assert returns is True


@mock.patch('assetallocation_arp.data_etl.dal.arp_proc_caller.FundStrategy', autospec=True)
def test_insert_fund_strategy_results_returns_false_when_res_is_empty(MockFundStrategy, mock_call_proc):
    user_id = 'a'
    fund_strategy = MockFundStrategy('a', 'times', 1, 2)
    mock_call_proc.return_value = [{}]

    a = ArpProcCaller()
    returns = a.insert_fund_strategy_results(fund_strategy, user_id)

    assert returns is False


def test_select_fund_strategy_results_calls_call_proc(mock_call_proc):
    fund_name = 'b'
    strategy_name = 'times'
    strategy_version = 2
    mock_call_proc.return_value = []

    a = ArpProcCaller()
    a.select_fund_strategy_results(fund_name, strategy_name, strategy_version)

    mock_call_proc.assert_called_once_with(a, 'arp.select_fund_strategy_results',
                                           [fund_name, strategy_name, strategy_version])


def test_select_times_assets_returns_fund_strategy(mock_call_proc):
    fund_name = 'b'
    strategy_name = 'times'
    strategy_version = 1
    mock_call_proc.return_value = [mock.MagicMock(), mock.MagicMock(), mock.MagicMock()]

    with mock.patch('assetallocation_arp.data_etl.dal.arp_proc_caller.FundStrategy', autospec=True):
        a = ArpProcCaller()
        returns = a.select_fund_strategy_results(fund_name, strategy_name, strategy_version)

    assert isinstance(returns, FundStrategy)
