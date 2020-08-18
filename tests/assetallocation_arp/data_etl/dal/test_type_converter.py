import mock
from decimal import Decimal

from assetallocation_arp.data_etl.dal.type_converter import (ArpTypeConverter, FundStrategyAssetAnalytic,
                                                             FundStrategyAssetWeight)


def mock_fund_strategy_asset_weights(asset_ticker: str, strategy_weight: Decimal, implemented_weight: Decimal):
    MockFundStrategyAssetWeight = mock.create_autospec(FundStrategyAssetWeight)
    mock_fsaw = MockFundStrategyAssetWeight(asset_ticker, strategy_weight)
    mock_fsaw.asset_ticker = asset_ticker
    mock_fsaw.strategy_weight = strategy_weight
    mock_fsaw.implemented_weight = implemented_weight
    return mock_fsaw


def mock_fund_strategy_asset_analytic(asset_ticker: str, category: str, subcategory: str, value: Decimal):
    MockFundStrategyAssetAnalytic = mock.create_autospec(FundStrategyAssetAnalytic)
    mock_fsaa = MockFundStrategyAssetAnalytic(asset_ticker, category, subcategory, value)
    mock_fsaa.asset_ticker = asset_ticker
    mock_fsaa.category = category
    mock_fsaa.subcategory = subcategory
    mock_fsaa.value = value
    return mock_fsaa


def test_analytics_to_composite_returns_expected_value():
    mock_fsaa1 = mock_fund_strategy_asset_analytic('a', 'b', 'c', Decimal(1))
    mock_fsaa2 = mock_fund_strategy_asset_analytic('d', 'e', 'f', Decimal(2))

    returns = ArpTypeConverter.analytics_to_composite([mock_fsaa1, mock_fsaa2])

    expected = ['("a","b","c",1)', '("d","e","f",2)']
    assert expected == returns


def test_weight_to_composite_returns_expected_value():
    mock_fsaa1 = mock_fund_strategy_asset_weights('a', Decimal(1), Decimal(2))
    mock_fsaa2 = mock_fund_strategy_asset_weights('c', Decimal(4), Decimal(3))

    returns = ArpTypeConverter.weights_to_composite([mock_fsaa1, mock_fsaa2])

    expected = ['("a",1,2)', '("c",4,3)']
    assert expected == returns