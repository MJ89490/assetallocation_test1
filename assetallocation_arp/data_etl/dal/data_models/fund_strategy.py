from datetime import date
from typing import List, Union, Optional
import configparser
from pathlib import Path

from numpy import nan

from assetallocation_arp.common_libraries.dal_enums.strategy import Name, Frequency
from assetallocation_arp.common_libraries.dal_enums.fund_strategy import Category, Performance, Signal, AggregationLevel
from assetallocation_arp.common_libraries.dal_enums.asset import Subcategory as AssetSubcategory


# noinspection PyAttributeOutsideInit
class FundStrategy:
    _config = configparser.ConfigParser()
    _config.read(Path(__file__).parents[4] / '.bumpversion.cfg')
    _python_code_version = _config['bumpversion']['current_version']

    def __init__(
            self, fund_name: str, strategy_name: Union[str, Name], strategy_version: int, weight: float,
            analytics: List['FundStrategyAnalytic'] = None, asset_weights: List['FundStrategyAssetWeight'] = None
    ) -> None:
        """FundStrategy class to hold data from database"""
        self.fund_name = fund_name
        self.strategy_name = strategy_name
        self.weight = weight
        self.strategy_version = strategy_version
        self.asset_weights = asset_weights or []
        self.analytics = analytics or []

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
    def analytics(self) -> List['FundStrategyAnalytic']:
        return self._analytics

    @analytics.setter
    def analytics(self, x: List['FundStrategyAnalytic']) -> None:
        self._analytics = x

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
    def weight(self) -> float:
        return self._weight

    @weight.setter
    def weight(self, x: float) -> None:
        self._weight = x

    def add_analytics(self, asset_analytics: List['FundStrategyAnalytic']) -> None:
        self._analytics.extend(asset_analytics)

    def add_analytic(self, asset_analytic: 'FundStrategyAnalytic') -> None:
        self._analytics.append(asset_analytic)

    def add_asset_weight(self, asset_weight: 'FundStrategyAssetWeight') -> None:
        self._asset_weights.append(asset_weight)


# noinspection PyAttributeOutsideInit
class FundStrategyAssetWeight:
    def __init__(
            self, asset_subcategory: Union[str, AssetSubcategory], business_date: date, theoretical_weight: float,
            frequency: Union[str, Frequency], ticker: Optional[str] = None
    ) -> None:
        """FundStrategyAssetWeight class to hold data from database"""
        self.asset_subcategory = asset_subcategory
        self.business_date = business_date
        self.frequency = frequency
        self.strategy_weight = theoretical_weight
        self.implemented_weight = nan
        self.ticker = ticker

    @property
    def business_date(self) -> date:
        return self._business_date

    @business_date.setter
    def business_date(self, x: date) -> None:
        self._business_date = x

    @property
    def implemented_weight(self) -> Optional[float]:
        return self._implemented_weight

    @implemented_weight.setter
    def implemented_weight(self, x: Optional[float]) -> None:
        self._implemented_weight = x

    @property
    def strategy_weight(self) -> float:
        return self._strategy_weight

    @strategy_weight.setter
    def strategy_weight(self, x: float) -> None:
        self._strategy_weight = x

    @property
    def frequency(self) -> Frequency:
        return self._frequency

    @frequency.setter
    def frequency(self, x: Union[str, Frequency]) -> None:
        self._frequency = x if isinstance(x, Frequency) else Frequency[x]

    @property
    def asset_subcategory(self) -> str:
        return self._asset_subcategory

    @asset_subcategory.setter
    def asset_subcategory(self, x: Union[str, AssetSubcategory]):
        self._asset_subcategory = x if isinstance(x, str) else x.name


# noinspection PyAttributeOutsideInit
class FundStrategyAnalytic:
    def __init__(
            self,  business_date: date, category: Union[str, Category], subcategory: Union[str, Performance, Signal],
            value: float, frequency: Union[str, Frequency], aggregation_level: Union[None, str, AggregationLevel] = None,
            comparator_name: Optional[str] = None
    ) -> None:
        """FundStrategyAnalytic class to hold data from database"""
        self.business_date = business_date
        self.category = category
        self.frequency = frequency
        self.subcategory = subcategory
        self.value = value
        self.aggregation_level = aggregation_level
        self.comparator_name = comparator_name

    @property
    def comparator_name(self) -> Optional[str]:
        return self._comparator_name

    @comparator_name.setter
    def comparator_name(self, x: str) -> None:
        if self.aggregation_level == AggregationLevel.comparator:
            self._comparator_name = x
        else:
            self._comparator_name = None


    @property
    def aggregation_level(self) -> AggregationLevel:
        return self._aggregation_level

    @aggregation_level.setter
    def aggregation_level(self, x: Union[None, str, AggregationLevel]) -> None:
        """default level of strategy"""
        if x is None:
            self._aggregation_level = AggregationLevel.strategy
        else:
            self._aggregation_level = x if isinstance(x, AggregationLevel) else AggregationLevel[x]

    @property
    def business_date(self) -> date:
        return self._business_date

    @business_date.setter
    def business_date(self, x: date) -> None:
        self._business_date = x

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
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, x: float):
        self._value = x

    @property
    def frequency(self) -> Frequency:
        return self._frequency

    @frequency.setter
    def frequency(self, x: Union[str, Frequency]) -> None:
        self._frequency = x if isinstance(x, Frequency) else Frequency[x]


# noinspection PyAttributeOutsideInit
class FundStrategyAssetAnalytic(FundStrategyAnalytic):
    def __init__(
            self, asset_ticker: str, asset_subcategory: Union[str, AssetSubcategory], business_date: date, category: Union[str, Category],
            subcategory: Union[str, Performance, Signal], value: float, frequency: Union[str, Frequency]
    ) -> None:
        """FundStrategyAssetAnalytic class to hold data from database"""
        super().__init__(business_date, category, subcategory, value, frequency)
        self.asset_subcategory = asset_subcategory
        self.asset_ticker = asset_ticker

    @property
    def asset_ticker(self) -> Optional[str]:
        return self._asset_ticker

    @asset_ticker.setter
    def asset_ticker(self, x: Optional[str]) -> None:
        self._asset_ticker = x

    @property
    def asset_subcategory(self) -> str:
        return self._asset_subcategory

    @asset_subcategory.setter
    def asset_subcategory(self, x: Union[str, AssetSubcategory]):
        self._asset_subcategory = x if isinstance(x, str) else x.name

    @property
    def aggregation_level(self) -> AggregationLevel:
        return AggregationLevel.asset

    @aggregation_level.setter
    def aggregation_level(self, x: Union[None, str, AggregationLevel]) -> None:
        """default level of asset"""
        if x in (None, AggregationLevel.asset, AggregationLevel.asset.name):
            self._aggregation_level = AggregationLevel.asset
        else:
            raise ValueError(f'FundStrategyAssetAnalytic must have an AggregationLevel of {AggregationLevel.asset.name}')
