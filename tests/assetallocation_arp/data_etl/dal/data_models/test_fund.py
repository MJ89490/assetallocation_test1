from pytest import raises

from assetallocation_arp.data_etl.dal.data_models.fund import Fund
from assetallocation_arp.common_libraries.dal_enums.currency import Currency


def test_currency_setter_raises_key_error_invalid_currency():
    with raises(KeyError):
        Fund('a', 'invalid_currency')


def test_currency_setter_sets_currency_valid_currency():
    currency = Currency.EUR.name

    f = Fund('a', currency)

    assert f.currency.name == currency
