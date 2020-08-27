from datetime import datetime

from pytest import raises


from assetallocation_arp.data_etl.dal.data_models.asset_analytic import AssetAnalytic, Category


def test_category_setter_raises_key_error_invalid_category():
    with raises(KeyError):
        AssetAnalytic('a', 'invalid_category', datetime(2020, 1, 1), float(1))


def test_category_setter_sets_category_valid_str_category():
    category = 'PX_MID'

    a = AssetAnalytic('a', category, datetime(2020, 1, 1), float(1))
    assert a.category.name == category


def test_category_setter_sets_category_valid_enum_category():
    category = Category['PX_MID']

    a = AssetAnalytic('a', category, datetime(2020, 1, 1), float(1))
    assert a.category == category
