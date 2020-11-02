import mock

from pytest import raises
from datetime import date

from assetallocation_arp.data_etl.dal.data_models.fund_strategy import FundStrategy, FundStrategyAssetAnalytic


def test_strategy_name_setter_raises_key_error_invalid_strategy_name():
    with raises(KeyError):
        FundStrategy('a', 'invalid_strategy_name', 1, float(1))


def test_strategy_name_setter_sets_strategy_name_valid_strategy_name():
    strategy_name = 'times'

    fs = FundStrategy('a', strategy_name, 1, float(1))

    assert fs.strategy_name.name == strategy_name


def test_add_fund_strategy_asset_analytic_adds_analytic():
    fsaa_path = 'assetallocation_arp.data_etl.dal.data_models.fund_strategy.FundStrategyAssetAnalytic'
    with mock.patch(fsaa_path, autospec=True) as MockFundStrategyAssetAnalytic:
        fs = FundStrategy('a', 'times', 1, float(1))
        fsaa = MockFundStrategyAssetAnalytic('a', date(2020, 1, 1), 'b', 'c', float(1), 'b')

        fs.add_fund_strategy_asset_analytic(fsaa)

        assert fsaa == fs.analytics[0]


def test_add_fund_strategy_asset_weight_adds_weight():
    fsaw_path = 'assetallocation_arp.data_etl.dal.data_models.fund_strategy.FundStrategyAssetWeight'
    with mock.patch(fsaw_path, autospec=True) as MockFundStrategyAssetWeight:
        fs = FundStrategy('a', 'times', 1, float(1))
        fsaw = MockFundStrategyAssetWeight('a', date(2020, 1, 1), float(1), 'b')

        fs.add_fund_strategy_asset_weight(fsaw)

        assert fsaw == fs.asset_weights[0]


def test_category_setter_raises_key_error_invalid_category():
    with raises(KeyError):
        FundStrategyAssetAnalytic('a', date(2020, 1, 1), 'invalid_category', 'carry', float(1), 'b')


def test_category_setter_sets_category_valid_category():
    category = 'performance'

    fass = FundStrategyAssetAnalytic('a', date(2020, 1, 1), category, 'carry', float(1), 'weekly')

    assert fass.category.name == category


def test_subcategory_setter_raises_key_error_invalid_subcategory_for_performance():
    with raises(KeyError):
        FundStrategyAssetAnalytic('a', date(2020, 1, 1), 'performance', 'momentum', float(1), 'b')


def test_subcategory_setter_raises_key_error_invalid_subcategory_for_signal():
    with raises(KeyError):
        FundStrategyAssetAnalytic('a', date(2020, 1, 1), 'signal', 'spot', float(1), 'b')


def test_subcategory_setter_sets_subcategory_valid_subcategory_for_performance():
    category = 'performance'
    subcategory = 'spot'

    fass = FundStrategyAssetAnalytic('a', date(2020, 1, 1), category, subcategory, float(1), 'weekly')

    assert fass.subcategory.name == subcategory


def test_subcategory_setter_sets_subcategory_valid_subcategory_for_signal():
    category = 'signal'
    subcategory = 'momentum'

    fass = FundStrategyAssetAnalytic('a', date(2020, 1, 1), category, subcategory, float(1), 'weekly')

    assert fass.subcategory.name == subcategory
