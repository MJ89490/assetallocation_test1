from decimal import Decimal
from typing import Union

from assetallocation_arp.common_enums.source import Source
from assetallocation_arp.common_enums.asset_analytic import Category


class AssetAnalytic:
    def __init__(self, asset_ticker: str, source: Union[str, Source], category: Union[str, Category], value: Decimal):
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
    def category(self, x: Union[str, Category]):
        self._category = x if isinstance(x, Category) else Category[x]

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, x: Union[str, Source]):
        self._source = x if isinstance(x, Source) else Source[x]

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, x):
        self._value = x
