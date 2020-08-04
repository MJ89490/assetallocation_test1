from decimal import Decimal

from assetallocation_arp.common_enums.source import Source
from assetallocation_arp.common_enums.asset_analytic import Category
from assetallocation_arp.data_etl.dal.validate import check_value


# TODO work out how to correctly type hint enum
class AssetAnalytic:
    def __init__(self, asset_ticker: str, source: Source, category: Category, value: Decimal):
        self._asset_ticker = asset_ticker
        self._source = source
        self._category = category
        self._value = value

    @property
    def asset_ticker(self):
        return self._asset_ticker

    @asset_ticker.setter
    def asset_ticker(self, x):
        self._asset_ticker = x

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, x: Category):
        check_value(x, Category.__members__.keys())
        self._category = x

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, x: Source):
        check_value(x, Source.__members__.keys())
        self._source = x

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, x):
        self._value = x
