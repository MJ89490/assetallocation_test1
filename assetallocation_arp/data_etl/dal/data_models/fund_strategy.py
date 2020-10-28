from datetime import date
from typing import List, Union, Optional, Tuple
import configparser
from pathlib import Path

from numpy import nan

from assetallocation_arp.common_libraries.dal_enums.strategy import Name
from assetallocation_arp.common_libraries.dal_enums.fund_strategy import Category, Performance, Signal
from assetallocation_arp.data_etl.dal.data_models.asset import Asset


# noinspection PyAttributeOutsideInit
class FundStrategy:
    _config = configparser.ConfigParser()
    _config.read(Path(__file__).parents[4] / '.bumpversion.cfg')
    _python_code_version = _config['bumpversion']['current_version']

    def __init__(self, fund_name: str, strategy_name: Union[str, Name], strategy_version: int, weight: float,
                 fund_strategy_asset_analytics: List['FundStrategyAssetAnalytic'] = None,
                 fund_strategy_asset_weights: List['FundStrategyAssetWeight'] = None):
        """FundStrategy class to hold data from database"""
        self.fund_name = fund_name
        self.strategy_name = strategy_name
        self.weight = weight
        self.output_is_saved = True
        self.strategy_version = strategy_version
        self.asset_weights = fund_strategy_asset_weights or []
        self.asset_analytics = fund_strategy_asset_analytics or []
        self._assets = []

    @property
    def assets(self) -> List[Asset]:
        return self._assets

    @assets.setter
    def assets(self, x: List[Asset]) -> None:
        unique_x = []
        for i in x:
            if i not in unique_x:
                unique_x.append(i)

        self._assets = unique_x

    def add_asset_if_not_exists(self, x: Asset) -> None:
        if x not in self.assets:
            self.assets.append(x)

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
        FundStrategyAssetWeight.check_unique(x)
        self._asset_weights = x

    @property
    def asset_analytics(self) -> List['FundStrategyAssetAnalytic']:
        return self._asset_analytics

    @asset_analytics.setter
    def asset_analytics(self, x: List['FundStrategyAssetAnalytic']) -> None:
        FundStrategyAssetAnalytic.check_unique(x)
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
    def output_is_saved(self) -> bool:
        return self._output_is_saved

    @output_is_saved.setter
    def output_is_saved(self, x: bool) -> None:
        self._output_is_saved = x

    @property
    def weight(self) -> float:
        return self._weight

    @weight.setter
    def weight(self, x: float) -> None:
        self._weight = x

    def add_fund_strategy_asset_analytics(self, asset_analytics: List['FundStrategyAssetAnalytic']) -> None:
        FundStrategyAssetAnalytic.check_unique(self.asset_analytics + asset_analytics)
        self._asset_analytics.extend(asset_analytics)

    def add_fund_strategy_asset_analytic(self, asset_analytic: 'FundStrategyAssetAnalytic') -> None:
        FundStrategyAssetAnalytic.check_unique(self.asset_analytics + [asset_analytic])
        self._asset_analytics.append(asset_analytic)

    def add_fund_strategy_asset_weight(self, asset_weight: 'FundStrategyAssetWeight') -> None:
        FundStrategyAssetWeight.check_unique(self.asset_weights + [asset_weight])
        self._asset_weights.append(asset_weight)


# noinspection PyAttributeOutsideInit
class FundStrategyAssetWeight:
    def __init__(self, asset_ticker: str, business_date: date, strategy_weight: float):
        """FundStrategyAssetWeight class to hold data from database"""
        self._asset_ticker = asset_ticker
        self.business_date = business_date
        self.strategy_weight = strategy_weight
        self.implemented_weight = nan

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
    def asset_ticker(self) -> str:
        return self._asset_ticker

    @asset_ticker.setter
    def asset_ticker(self, x: str) -> None:
        self._asset_ticker = x

    @staticmethod
    def check_unique(asset_weights: List['FundStrategyAssetWeight']) -> None:
        if len(set((i.asset_ticker, i.business_date) for i in asset_weights)) != len(asset_weights):
            raise ValueError('Duplicate asset_ticker, business_date combinations are not allowed')


# noinspection PyAttributeOutsideInit
class FundStrategyAssetAnalytic:
    def __init__(self,  asset_ticker: str, business_date: date, category: Union[str, Category],
                 subcategory: Union[str, Performance, Signal],
                 value: float) -> None:
        """FundStrategyAssetAnalytic class to hold data from database"""
        self.asset_ticker = asset_ticker
        self.business_date = business_date
        self.category = category
        self.subcategory = subcategory
        self.value = value

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
    def asset_ticker(self) -> str:
        return self._asset_ticker

    @asset_ticker.setter
    def asset_ticker(self, x: str):
        self._asset_ticker = x

    @staticmethod
    def check_unique(asset_analytics: List['FundStrategyAssetAnalytic']) -> None:
        if len(set((i.asset_ticker, i.business_date, i.category, i.subcategory) for i in asset_analytics)) != len(asset_analytics):
            raise ValueError('Duplicate asset_ticker, business_date, category, subcategory combinations are not allowed')