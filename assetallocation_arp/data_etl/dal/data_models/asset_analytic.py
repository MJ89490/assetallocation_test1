from typing import Union
from datetime import datetime

from assetallocation_arp.common_libraries.dal_enums.asset_analytic import Category


# noinspection PyAttributeOutsideInit
class AssetAnalytic:
    def __init__(self, asset_ticker: str, category: Union[str, Category],
                 business_datetime: datetime, value: float) -> None:
        """AssetAnalytic class to hold data from database"""
        self.asset_ticker = asset_ticker
        self.category = category
        self.business_datetime = business_datetime
        self.value = value

    @property
    def business_datetime(self) -> datetime:
        return self._business_datetime

    @business_datetime.setter
    def business_datetime(self, x: datetime) -> None:
        self._business_datetime = x

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
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, x:  float) -> None:
        self._value = x
