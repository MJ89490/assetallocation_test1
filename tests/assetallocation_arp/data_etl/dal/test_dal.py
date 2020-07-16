from pytest import fixture, raises
from pandas import DataFrame, testing

from assetallocation_arp.data_etl.dal.dal import class_attributes_to_df


class A:
    def __init__(self, a, b) -> None:
        self.a = a
        self.b = b


class B:
    def __init__(self, b, c) -> None:
        self._b = b
        self._c = c


def test_class_attributes_to_df_raises_error_different_types():
    with raises(TypeError):
        class_attributes_to_df([A(1, 2), B(1, 2)])


def test_class_attributes_to_df_creates_df_with_columns_named_after_attributes():
    expected = DataFrame([[1, 2], [2, 3]], columns=['a', 'b'])
    returns = class_attributes_to_df([A(1, 2), A(2, 3)])

    testing.assert_frame_equal(expected, returns)


def test_class_attributes_to_df_creates_df_private_attribute_columns_named_without_leading_underscore():
    expected = DataFrame([[1, 2], [2, 3]], columns=['b', 'c'])
    returns = class_attributes_to_df([B(1, 2), B(2, 3)])

    testing.assert_frame_equal(expected, returns)
