import mock
from datetime import date
from enum import Enum

from assetallocation_arp.data_etl.dal.type_converter import ArpTypeConverter
from assetallocation_arp.data_etl.dal.data_models.fund_strategy import FundStrategyAssetAnalytic, \
    FundStrategyAssetWeight, FundStrategyAnalytic


def mock_fund_strategy_asset_weights(asset_subcategory: str, business_date: date, strategy_weight: float,
                                     implemented_weight: float, frequency: str):
    MockFundStrategyAssetWeight = mock.create_autospec(FundStrategyAssetWeight)
    mock_fsaw = MockFundStrategyAssetWeight(asset_subcategory, business_date, strategy_weight, frequency)
    mock_fsaw.business_date = business_date
    mock_fsaw.asset_subcategory = asset_subcategory
    mock_fsaw.frequency.name = frequency
    mock_fsaw.strategy_weight = strategy_weight
    mock_fsaw.implemented_weight = implemented_weight
    return mock_fsaw


def mock_fund_strategy_asset_analytic(asset_subcategory: str, business_date: date, category: str, subcategory: str,
                                      value: float, frequency: str, aggregation_level: str):
    MockFundStrategyAssetAnalytic = mock.create_autospec(FundStrategyAssetAnalytic)
    mock_fsaa = MockFundStrategyAssetAnalytic(asset_subcategory, business_date, category, subcategory, value, frequency)
    mock_fsaa.asset_subcategory = asset_subcategory
    mock_fsaa.business_date = business_date
    mock_fsaa.category.name = category
    mock_fsaa.subcategory.name = subcategory
    mock_fsaa.frequency.name = frequency
    mock_fsaa.aggregation_level.name = aggregation_level
    mock_fsaa.value = value
    return mock_fsaa


def mock_fund_strategy_analytic(business_date: date, category: str, subcategory: str, value: float,
                                frequency: str, aggregation_level: str):
    MockFundStrategyAnalytic = mock.create_autospec(FundStrategyAnalytic)
    mock_fsa = MockFundStrategyAnalytic(business_date, category, subcategory, value, frequency)
    mock_fsa.business_date = business_date
    mock_fsa.category.name = category
    mock_fsa.subcategory.name = subcategory
    mock_fsa.frequency.name = frequency
    mock_fsa.aggregation_level.name = aggregation_level
    mock_fsa.value = value
    return mock_fsa


def test_strategy_asset_analytics_to_composite_returns_expected_value():
    mock_fsaa1 = mock_fund_strategy_asset_analytic('a', date(2020, 1, 2), 'b', 'c', float(1), 'g', 'i')
    mock_fsaa1.asset_ticker = 'z'
    mock_fsaa2 = mock_fund_strategy_asset_analytic('b', date(2020, 1, 3), 'e', 'f', float(2), 'h', 'j')
    mock_fsaa2.asset_ticker = 'y'
    returns = ArpTypeConverter._strategy_asset_analytics_to_composite([mock_fsaa1, mock_fsaa2])

    expected = ['("z","2020-01-02","b","c","g",1.0)', '("y","2020-01-03","e","f","h",2.0)']
    assert expected == returns


def test_strategy_analytics_to_composite_returns_expected_value():
    class TestEnum(Enum):
        cat = 1
        subcat = 2
        weekly = 3
        cat1 = 4
        subcat1 = 5
        daily = 6

    analytics = {
        (date(2020, 1, 2), TestEnum.cat, TestEnum.subcat, TestEnum.weekly): [1.0, None, None],
        (date(2020, 1, 3), TestEnum.cat1, TestEnum.subcat1, TestEnum.daily): [2.0, 'comp', 6.0]
    }

    returns = ArpTypeConverter._strategy_analytics_to_composite(analytics)

    expected = ['("2020-01-02","cat","subcat","weekly",1.0,,)', '("2020-01-03","cat1","subcat1","daily",2.0,"comp",6.0)']
    assert expected == returns


def test_weight_to_composite_returns_expected_value():
    mock_fsaa1 = mock_fund_strategy_asset_weights('a', date(2020, 1, 2), float(1), float(2), 'g')
    mock_fsaa2 = mock_fund_strategy_asset_weights('c', date(2020, 1, 3), float(4), float(3), 'h')

    returns = ArpTypeConverter.weights_to_composite([mock_fsaa1, mock_fsaa2])

    expected = ['("a","2020-01-02","g",1.0,2.0)', '("c","2020-01-03","h",4.0,3.0)']
    assert expected == returns