from typing import Union
from decimal import Decimal

from assetallocation_arp.data_etl.dal.validate import validate_enum
from assetallocation_arp.common_libraries.strategy_asset_analytic import Category, Performance, Signal


class StrategyAssetAnalytic:
    def __init__(self,  asset_ticker: str, category: Category, subcategory: Union[Performance, Signal], value: Decimal):
        self._asset_ticker = asset_ticker
        self.category = category
        self.subcategory = subcategory
        self._value = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, x):
        validate_enum(x, Category.__members__.keys())
        self._category = x

    @property
    def subcategory(self):
        return self._subcategory

    @subcategory.setter
    def subcategory(self, x):
        if self.category == Category.performance.name:
            valid_values = Performance.__members__.keys()
        else:
            valid_values = Signal.__members__.keys()

        validate_enum(x, valid_values)

        self._subcategory = x

    @property
    def value(self):
        return self._value

    @property
    def asset_ticker(self):
        return self._asset_ticker
