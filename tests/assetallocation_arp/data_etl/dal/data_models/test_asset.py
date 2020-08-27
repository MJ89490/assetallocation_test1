import mock

from pytest import mark, raises
from datetime import datetime

from assetallocation_arp.data_etl.dal.data_models.asset import Asset


def test_asset_country_setter_raises_key_error_invalid_country():
    with raises(KeyError):
        a = Asset('a', 'b')
        a.country = 'invalid_country'


def test_asset_country_setter_sets_country_valid_country():
    country = 'EU'

    a = Asset('a', 'b')
    a.country = country

    assert a.country.name == country


def test_asset_category_setter_raises_key_error_invalid_category():
    with raises(KeyError):
        a = Asset('a', 'b')
        a.category = 'invalid_category'


def test_asset_category_setter_sets_category_valid_category():
    category = 'FX'
    a = Asset('a', 'b')
    a.category = category

    assert a.category.name == category


def test_asset_currency_setter_raises_key_error_invalid_currency():
    with raises(KeyError):
        a = Asset('a', 'b')
        a.currency = 'invalid_currency'


def test_asset_currency_setter_sets_currency_valid_currency():
    currency = 'EUR'

    a = Asset('a', 'b')
    a.currency = currency

    assert a.currency.name == currency


@mark.parametrize('country, expected', [('EU', 'Europe'), ('US', 'North America')])
def test_asset_region_property_gets_region_based_on_country(country, expected):
    a = Asset('a', 'b')
    a.country = country
    assert expected == a.region


def test_asset_add_analytic_raises_error_if_tickers_do_not_match():
    with mock.patch('assetallocation_arp.data_etl.dal.data_models.asset.AssetAnalytic', autospec=True) as MockAssetAnalytic:
        a = Asset('a', 'FX')
        b = MockAssetAnalytic('not_a', 'b', datetime(2020, 1, 1), 1)
        b.asset_ticker = 'not_a'

        with raises(ValueError):
            a.add_analytic(b)


def test_asset_add_analytic_adds_analytic_if_tickers_match():
    asset_ticker = 'ticker1'

    with mock.patch('assetallocation_arp.data_etl.dal.data_models.asset.AssetAnalytic', autospec=True) as MockAssetAnalytic:
        a = Asset(asset_ticker, 'FX')
        b = MockAssetAnalytic(asset_ticker, 'b', datetime(2020, 1, 1), 1)
        b.asset_ticker = asset_ticker

        a.add_analytic(b)

        assert b == a.asset_analytics[0]
