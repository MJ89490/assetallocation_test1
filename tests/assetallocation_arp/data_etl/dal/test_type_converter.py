import mock
from datetime import date

from assetallocation_arp.data_etl.dal.type_converter import (ArpTypeConverter, FundStrategyAssetAnalytic,
                                                             FundStrategyAssetWeight)


def mock_fund_strategy_asset_weights(asset_ticker: str, business_date: date, strategy_weight: float, implemented_weight: float):
    MockFundStrategyAssetWeight = mock.create_autospec(FundStrategyAssetWeight)
    mock_fsaw = MockFundStrategyAssetWeight(asset_ticker, business_date, strategy_weight)
    mock_fsaw.business_date = business_date
    mock_fsaw.asset_ticker = asset_ticker
    mock_fsaw.strategy_weight = strategy_weight
    mock_fsaw.implemented_weight = implemented_weight
    return mock_fsaw


def mock_fund_strategy_asset_analytic(asset_ticker: str, business_date: date, category: str, subcategory: str, value: float):
    MockFundStrategyAssetAnalytic = mock.create_autospec(FundStrategyAssetAnalytic)
    mock_fsaa = MockFundStrategyAssetAnalytic(asset_ticker, business_date, category, subcategory, value)
    mock_fsaa.asset_ticker = asset_ticker
    mock_fsaa.business_date = business_date
    mock_fsaa.category.name = category
    mock_fsaa.subcategory.name = subcategory
    mock_fsaa.value = value
    return mock_fsaa


def test_analytics_to_composite_returns_expected_value():
    mock_fsaa1 = mock_fund_strategy_asset_analytic('a', date(2020, 1, 2), 'b', 'c', float(1))
    mock_fsaa2 = mock_fund_strategy_asset_analytic('d', date(2020, 1, 3), 'e', 'f', float(2))

    returns = ArpTypeConverter.analytics_to_composite([mock_fsaa1, mock_fsaa2])

    expected = ['("a","2020-01-02","b","c",1.0)', '("d","2020-01-03","e","f",2.0)']
    assert expected == returns


def test_weight_to_composite_returns_expected_value():
    mock_fsaa1 = mock_fund_strategy_asset_weights('a', date(2020, 1, 2), float(1), float(2))
    mock_fsaa2 = mock_fund_strategy_asset_weights('c', date(2020, 1, 3), float(4), float(3))

    returns = ArpTypeConverter.weights_to_composite([mock_fsaa1, mock_fsaa2])

    expected = ['("a","2020-01-02",1.0,2.0)', '("c","2020-01-03",4.0,3.0)']
    assert expected == returns