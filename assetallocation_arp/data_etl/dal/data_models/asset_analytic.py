from decimal import Decimal
from typing import Union

from common_libraries.dal_enums.source import Source
from common_libraries.dal_enums.asset_analytic import Category


# noinspection PyAttributeOutsideInit
class AssetAnalytic:
    def __init__(self, asset_ticker: str, source: Union[str, Source], category: Union[str, Category],
                 value: Decimal) -> None:
        """AssetAnalytic class to hold data from database"""
        self.asset_ticker = asset_ticker
        self.source = source
        self.category = category
        self.value = value

    @property
    def asset_ticker(self) -> str:
        return self._asset_ticker

    @asset_ticker.setter
    def asset_ticker(self, x: str) -> None:
        self._asset_ticker = x

    @property
    def category(self) -> Category:
        return self._category

    @category.setter
    def category(self, x: Union[str, Category]) -> None:
        self._category = x if isinstance(x, Category) else Category[x]

    @property
    def source(self) -> Source:
        return self._source

    @source.setter
    def source(self, x: Union[str, Source]) -> None:
        self._source = x if isinstance(x, Source) else Source[x]

    @property
    def value(self) -> Decimal:
        return self._value

    @value.setter
    def value(self, x:  Decimal) -> None:
        self._value = x
