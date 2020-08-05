from decimal import Decimal
from datetime import datetime
from typing import List, Union

from common_enums.strategy import Name
from common_enums.fund_strategy import Category, Performance, Signal


# TODO look into typing class attributes
class FundStrategy:
    def __init__(self, fund_name: str, strategy_name: Union[str, Name], strategy_version: int, weight: Decimal,
                 fund_strategy_asset_analytics: List['FundStrategyAssetAnalytic'] = None,
                 fund_strategy_asset_weights: List['FundStrategyAssetWeight'] = None):
        self._fund_name = fund_name
        self.strategy_name = strategy_name
        self._weight = weight
        self._output_is_saved = True
        self._business_datetime = datetime.now()
        self._python_code_version = '0'  # TODO set this somewhere to use code wide
        self._strategy_version = strategy_version
        self.asset_weights = fund_strategy_asset_weights or []
        self.asset_analytics = fund_strategy_asset_analytics or []

    @property
    def fund_name(self):
        return self._fund_name

    @fund_name.setter
    def fund_name(self, x):
        self._fund_name = x

    @property
    def python_code_version(self):
        return self._python_code_version

    @python_code_version.setter
    def python_code_version(self, x: str):
        self._python_code_version = x

    @property
    def asset_weights(self):
        return self._asset_weights

    @asset_weights.setter
    def asset_weights(self, x: List['FundStrategyAssetWeight']):
        self._asset_weights = x

    @property
    def asset_analytics(self):
        return self._asset_analytics

    @asset_analytics.setter
    def asset_analytics(self, x: List['FundStrategyAssetAnalytic']):
        self._asset_analytics = x

    @property
    def strategy_name(self):
        return self._strategy_name

    @strategy_name.setter
    def strategy_name(self, x: Union[str, Name]):
        self._strategy_name = x if isinstance(x, Name) else Name[x]

    @property
    def strategy_version(self):
        return self._strategy_version

    @strategy_version.setter
    def strategy_version(self, x: int):
        self._strategy_version = x

    @property
    def business_datetime(self):
        return self._business_datetime

    @business_datetime.setter
    def business_datetime(self, x: datetime):
        self._business_datetime = x

    @property
    def output_is_saved(self):
        return self._output_is_saved

    @output_is_saved.setter
    def output_is_saved(self, x: bool):
        self._output_is_saved = x

    @property
    def weight(self):
        return self._weight

    def add_fund_strategy_asset_analytic(self, fund_strategy_asset_analytic: 'FundStrategyAssetAnalytic'):
        self._asset_analytics.append(fund_strategy_asset_analytic)

    def add_fund_strategy_asset_weight(self, fund_strategy_asset_weight: 'FundStrategyAssetWeight'):
        self._asset_weights.append(fund_strategy_asset_weight)


class FundStrategyAssetWeight:
    def __init__(self, asset_ticker: str, strategy_weight: Decimal):
        self._asset_ticker = asset_ticker
        self._strategy_weight = strategy_weight
        self._implemented_weight = 0

    @property
    def implemented_weight(self):
        return self._implemented_weight

    @implemented_weight.setter
    def implemented_weight(self, x: Decimal):
        self._implemented_weight = x

    @property
    def strategy_weight(self):
        return self._strategy_weight

    @strategy_weight.setter
    def strategy_weight(self, x):
        self._strategy_weight = x

    @property
    def asset_ticker(self):
        return self._asset_ticker

    @asset_ticker.setter
    def asset_ticker(self, x):
        self._asset_ticker = x


class FundStrategyAssetAnalytic:
    def __init__(self,  asset_ticker: str, category: Union[str, Category], subcategory: Union[str, Performance, Signal],
                 value: Decimal):
        self._asset_ticker = asset_ticker
        self.category = category
        self.subcategory = subcategory
        self._value = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, x: Union[str, Category]):
        self._category = x if isinstance(x, Category) else Category[x]

    @property
    def subcategory(self):
        return self._subcategory

    @subcategory.setter
    def subcategory(self, x: Union[str, Performance, Signal]):
        if self.category is Category.performance:
            self._subcategory = x if isinstance(x, Performance) else Performance[x]
        else:
            self._subcategory = x if isinstance(x, Signal) else Signal[x]

    @property
    def value(self):
        return self._value

    @property
    def asset_ticker(self):
        return self._asset_ticker
