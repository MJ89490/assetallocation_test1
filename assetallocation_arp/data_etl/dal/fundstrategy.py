from decimal import Decimal
from datetime import datetime
from typing import List, Union
import configparser
from pathlib import Path

from common_enums.strategy import Name
from common_enums.fund_strategy import Category, Performance, Signal


# noinspection PyAttributeOutsideInit,PyAttributeOutsideInit,PyAttributeOutsideInit
class FundStrategy:
    _config = configparser.ConfigParser()
    _config.read(Path(__file__).parents[3] / '.bumpversion.cfg')
    _python_code_version = _config['bumpversion']['current_version']

    def __init__(self, fund_name: str, strategy_name: Union[str, Name], strategy_version: int, weight: Decimal,
                 fund_strategy_asset_analytics: List['FundStrategyAssetAnalytic'] = None,
                 fund_strategy_asset_weights: List['FundStrategyAssetWeight'] = None):
        self._fund_name = fund_name
        self.strategy_name = strategy_name
        self._weight = weight
        self._output_is_saved = True
        self._business_datetime = datetime.now()
        self._strategy_version = strategy_version
        self.asset_weights = fund_strategy_asset_weights or []
        self.asset_analytics = fund_strategy_asset_analytics or []

    @property
    def fund_name(self) -> str:
        return self._fund_name

    @fund_name.setter
    def fund_name(self, x) -> None:
        self._fund_name = x

    @property
    def python_code_version(self) -> str:
        return self._python_code_version

    @python_code_version.setter
    def python_code_version(self, x: str) -> None:
        self._python_code_version = x

    @property
    def asset_weights(self) -> List['FundStrategyAssetWeight']:
        return self._asset_weights

    @asset_weights.setter
    def asset_weights(self, x: List['FundStrategyAssetWeight']) -> None:
        self._asset_weights = x

    @property
    def asset_analytics(self) -> List['FundStrategyAssetAnalytic']:
        return self._asset_analytics

    @asset_analytics.setter
    def asset_analytics(self, x: List['FundStrategyAssetAnalytic']) -> None:
        self._asset_analytics = x

    @property
    def strategy_name(self) -> Name:
        return self._strategy_name

    @strategy_name.setter
    def strategy_name(self, x: Union[str, Name]) -> None:
        self._strategy_name = x if isinstance(x, Name) else Name[x]

    @property
    def strategy_version(self) -> int:
        return self._strategy_version

    @strategy_version.setter
    def strategy_version(self, x: int) -> None:
        self._strategy_version = x

    @property
    def business_datetime(self) -> datetime:
        return self._business_datetime

    @business_datetime.setter
    def business_datetime(self, x: datetime) -> None:
        self._business_datetime = x

    @property
    def output_is_saved(self) -> bool:
        return self._output_is_saved

    @output_is_saved.setter
    def output_is_saved(self, x: bool) -> None:
        self._output_is_saved = x

    @property
    def weight(self) -> Decimal:
        return self._weight

    @weight.setter
    def weight(self, x: Decimal) -> None:
        self._weight = x

    def add_fund_strategy_asset_analytic(self, fund_strategy_asset_analytic: 'FundStrategyAssetAnalytic') -> None:
        self._asset_analytics.append(fund_strategy_asset_analytic)

    def add_fund_strategy_asset_weight(self, fund_strategy_asset_weight: 'FundStrategyAssetWeight') -> None:
        self._asset_weights.append(fund_strategy_asset_weight)


class FundStrategyAssetWeight:
    def __init__(self, asset_ticker: str, strategy_weight: Decimal):
        self._asset_ticker = asset_ticker
        self._strategy_weight = strategy_weight
        self._implemented_weight = Decimal(0)

    @property
    def implemented_weight(self) -> Decimal:
        return self._implemented_weight

    @implemented_weight.setter
    def implemented_weight(self, x: Decimal) -> None:
        self._implemented_weight = x

    @property
    def strategy_weight(self) -> Decimal:
        return self._strategy_weight

    @strategy_weight.setter
    def strategy_weight(self, x: Decimal) -> None:
        self._strategy_weight = x

    @property
    def asset_ticker(self) -> str:
        return self._asset_ticker

    @asset_ticker.setter
    def asset_ticker(self, x: str) -> None:
        self._asset_ticker = x


# noinspection PyAttributeOutsideInit,PyAttributeOutsideInit,PyAttributeOutsideInit,PyAttributeOutsideInit
class FundStrategyAssetAnalytic:
    def __init__(self,  asset_ticker: str, category: Union[str, Category], subcategory: Union[str, Performance, Signal],
                 value: Decimal) -> None:
        self.asset_ticker = asset_ticker
        self.category = category
        self.subcategory = subcategory
        self.value = value

    @property
    def category(self) -> Category:
        return self._category

    @category.setter
    def category(self, x: Union[str, Category]) -> None:
        self._category = x if isinstance(x, Category) else Category[x]

    @property
    def subcategory(self) -> Union[Performance, Signal]:
        return self._subcategory

    @subcategory.setter
    def subcategory(self, x: Union[str, Performance, Signal]) -> None:
        if self.category is Category.performance:
            self._subcategory = x if isinstance(x, Performance) else Performance[x]
        else:
            self._subcategory = x if isinstance(x, Signal) else Signal[x]

    @property
    def value(self) -> Decimal:
        return self._value

    @value.setter
    def value(self, x: Decimal):
        self._value = x

    @property
    def asset_ticker(self) -> str:
        return self._asset_ticker

    @asset_ticker.setter
    def asset_ticker(self, x: str):
        self._asset_ticker = x