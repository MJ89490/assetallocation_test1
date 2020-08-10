from decimal import Decimal
import mock

from pytest import raises

from assetallocation_arp.data_etl.dal.data_models.fund_strategy import FundStrategy, FundStrategyAssetAnalytic


def test_strategy_name_setter_raises_key_error_invalid_strategy_name():
    with raises(KeyError):
        FundStrategy('a', 'invalid_strategy_name', 1, Decimal(1))


def test_strategy_name_setter_sets_strategy_name_valid_strategy_name():
    strategy_name = 'times'

    fs = FundStrategy('a', strategy_name, 1, Decimal(1))

    assert fs.strategy_name.name == strategy_name


def test_add_fund_strategy_asset_analytic_adds_analytic():
    fsaa_path = 'assetallocation_arp.data_etl.dal.data_models.fund_strategy.FundStrategyAssetAnalytic'
    with mock.patch(fsaa_path, autospec=True) as MockFundStrategyAssetAnalytic:
        fs = FundStrategy('a', 'times', 1, Decimal(1))
        fsaa = MockFundStrategyAssetAnalytic('a', 'b', 'c', Decimal(1))

        fs.add_fund_strategy_asset_analytic(fsaa)

        assert fsaa == fs.asset_analytics[0]


def test_add_fund_strategy_asset_weight_adds_weight():
    fsaw_path = 'assetallocation_arp.data_etl.dal.data_models.fund_strategy.FundStrategyAssetWeight'
    with mock.patch(fsaw_path, autospec=True) as MockFundStrategyAssetWeight:
        fs = FundStrategy('a', 'times', 1, Decimal(1))
        fsaw = MockFundStrategyAssetWeight('a', Decimal(1))

        fs.add_fund_strategy_asset_weight(fsaw)

        assert fsaw == fs.asset_weights[0]


def test_category_setter_raises_key_error_invalid_category():
    with raises(KeyError):
        FundStrategyAssetAnalytic('a', 'invalid_category', 'carry', Decimal(1))


def test_category_setter_sets_category_valid_category():
    category = 'performance'

    fass = FundStrategyAssetAnalytic('a', category, 'carry', Decimal(1))

    assert fass.category.name == category


def test_subcategory_setter_raises_key_error_invalid_subcategory_for_performance():
    with raises(KeyError):
        FundStrategyAssetAnalytic('a', 'performance', 'momentum', Decimal(1))


def test_subcategory_setter_raises_key_error_invalid_subcategory_for_signal():
    with raises(KeyError):
        FundStrategyAssetAnalytic('a', 'signal', 'spot', Decimal(1))


def test_subcategory_setter_sets_subcategory_valid_subcategory_for_performance():
    category = 'performance'
    subcategory = 'spot'

    fass = FundStrategyAssetAnalytic('a', category, subcategory, Decimal(1))

    assert fass.subcategory.name == subcategory


def test_subcategory_setter_sets_subcategory_valid_subcategory_for_signal():
    category = 'signal'
    subcategory = 'momentum'

    fass = FundStrategyAssetAnalytic('a', category, subcategory, Decimal(1))

    assert fass.subcategory.name == subcategory