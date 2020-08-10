import mock

from pytest import mark, raises

from assetallocation_arp.data_etl.dal.data_models.asset import Asset


def test_asset_country_setter_raises_key_error_invalid_country():
    with raises(KeyError):
        Asset('a', 'FX', 'invalid_country', 'EUR', 'e', 'f')


def test_asset_country_setter_sets_country_valid_country():
    country = 'EU'

    a = Asset('a', 'FX', country, 'EUR', 'e', 'f')

    assert a.country.name == country


def test_asset_category_setter_raises_key_error_invalid_category():
    with raises(KeyError):
        Asset('a', 'invalid_category', 'EU', 'EUR', 'e', 'f')


def test_asset_category_setter_sets_category_valid_category():
    category = 'FX'

    a = Asset('a', category, 'EU', 'EUR', 'e', 'f')

    assert a.category.name == category


def test_asset_currency_setter_raises_key_error_invalid_currency():
    with raises(KeyError):
        Asset('a', 'FX', 'EU', 'invalid_currency', 'e', 'f')


def test_asset_currency_setter_sets_currency_valid_currency():
    currency = 'EUR'

    a = Asset('a', 'FX', 'EU', currency, 'e', 'f')

    assert a.currency.name == currency


@mark.parametrize('country, expected', [('EU', 'Europe'), ('US', 'North America')])
def test_asset_region_setter_sets_region_based_on_country(country, expected):
    a = Asset('a', 'FX', country, 'EUR', 'e', 'f')
    assert expected == a.region


def test_asset_add_analytic_raises_error_if_tickers_do_not_match():
    with mock.patch('assetallocation_arp.data_etl.dal.data_models.asset.AssetAnalytic', autospec=True) as MockAssetAnalytic:
        a = Asset('a', 'FX', 'EU', 'EUR', 'e', 'f')
        b = MockAssetAnalytic('not_a', 'b', 'c', 1)
        b.asset_ticker = 'not_a'

        with raises(ValueError):
            a.add_analytic(b)


def test_asset_add_analytic_adds_analytic_if_tickers_match():
    asset_ticker = 'ticker1'

    with mock.patch('assetallocation_arp.data_etl.dal.data_models.asset.AssetAnalytic', autospec=True) as MockAssetAnalytic:
        a = Asset(asset_ticker, 'FX', 'EU', 'EUR', 'e', 'f')
        b = MockAssetAnalytic(asset_ticker, 'b', 'c', 1)
        b.asset_ticker = asset_ticker

        a.add_analytic(b)

        assert b == a.asset_analytics[0]
