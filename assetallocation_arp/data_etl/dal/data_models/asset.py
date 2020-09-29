from typing import List, Union

from assetallocation_arp.common_libraries.dal_enums.asset import Category
from assetallocation_arp.common_libraries.dal_enums.currency import Currency
from assetallocation_arp.common_libraries.dal_enums.country import Country, country_region
from assetallocation_arp.data_etl.dal.data_models.asset_analytic import AssetAnalytic
from assetallocation_arp.data_etl.dal.data_models.custom_error import IncorrectTickerError


# noinspection PyAttributeOutsideInit
class Asset:
    def __init__(self, ticker: str):
        """Asset class to hold data from database"""
        self._category = None
        self._country = None
        self._currency = None
        self.description = ''
        self._name = None
        self.ticker = ticker
        self._is_tr = None
        self._subcategory = None
        self.asset_analytics = []

    @property
    def ticker(self) -> str:
        return self._ticker

    @ticker.setter
    def ticker(self, x: str) -> None:
        self._ticker = x

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, x: str) -> None:
        self._name = x

    @property
    def asset_analytics(self) -> List[AssetAnalytic]:
        return self._asset_analytics

    @asset_analytics.setter
    def asset_analytics(self, x: List[AssetAnalytic]) -> None:
        self._asset_analytics = x

    @property
    def category(self) -> Category:
        return self._category

    @category.setter
    def category(self, x: Union[str, Category]) -> None:
        self._category = x if isinstance(x, Category) else Category[x]

    @property
    def country(self) -> Country:
        return self._country

    @country.setter
    def country(self, x: Union[str, Country]) -> None:
        self._country = x if isinstance(x, Country) else Country[x]

    @property
    def region(self) -> str:
        return country_region.get(self.country.name)

    @property
    def subcategory(self) -> str:
        return self._subcategory

    @subcategory.setter
    def subcategory(self, x: str):
        self._subcategory = x

    @property
    def currency(self) -> Currency:
        return self._currency

    @currency.setter
    def currency(self, x: Union[str, Currency]) -> None:
        self._currency = x if isinstance(x, Currency) else Currency[x]

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, x: str) -> None:
        self._description = x

    @property
    def is_tr(self) -> bool:
        return self._is_tr

    @is_tr.setter
    def is_tr(self, x: bool) -> None:
        self._is_tr = x

    def add_analytic(self, asset_analytic: AssetAnalytic) -> None:
        if asset_analytic.asset_ticker == self.ticker:
            self._asset_analytics.append(asset_analytic)
        else:
            raise IncorrectTickerError({'asset': self.ticker, 'asset_analytic': asset_analytic.asset_ticker})

    def __eq__(self, other: 'Asset'):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False


class FicaAsset(Asset):
    def __init__(self, ticker: str, category: Union[str, Category], country: Union[str, Country],
                 currency: Union[str, Currency], name: str, type: str, future_ticker: str,
                 generic_yield_ticker: str) -> None:
        """FicaAsset class to hold data from database"""
        super().__init__(ticker)
        super().name = name
        self._future_ticker = future_ticker
        self._generic_yield_ticker = generic_yield_ticker

    @property
    def generic_yield_ticker(self) -> str:
        return self._generic_yield_ticker

    @generic_yield_ticker.setter
    def generic_yield_ticker(self, x: str) -> None:
        self._generic_yield_ticker = x


# noinspection PyAttributeOutsideInit
class TimesAssetInput:
    def __init__(self, s_leverage: int, signal_ticker: str, future_ticker: str, cost: float) -> None:
        """TimesAssetInput class to hold data from database"""
        self.signal_ticker = signal_ticker
        self.future_ticker = future_ticker
        self.cost = cost
        self.s_leverage = s_leverage
        self._signal_asset = None
        self._future_asset = None

    @property
    def signal_asset(self) -> Asset:
        return self._signal_asset

    @signal_asset.setter
    def signal_asset(self, x: Asset) -> None:
        if x.ticker == self.signal_ticker:
            self._signal_asset = x
        else:
            raise IncorrectTickerError({'asset': x.ticker, 'signal': self.signal_ticker})

    @property
    def future_asset(self) -> Asset:
        return self._future_asset

    @future_asset.setter
    def future_asset(self, x: Asset) -> None:
        if x.ticker == self.future_ticker:
            self._future_asset = x
        else:
            raise IncorrectTickerError({'asset': x.ticker, 'future': self.future_ticker})

    @property
    def s_leverage(self) -> int:
        return self._s_leverage

    @s_leverage.setter
    def s_leverage(self, x: int) -> None:
        self._s_leverage = x

    @property
    def signal_ticker(self) -> str:
        return self._signal_ticker

    @signal_ticker.setter
    def signal_ticker(self, x: str) -> None:
        self._signal_ticker = x

    @property
    def future_ticker(self) -> str:
        return self._future_ticker

    @future_ticker.setter
    def future_ticker(self, x: str) -> None:
        self._future_ticker = x

    @property
    def cost(self) -> float:
        return self._cost

    @cost.setter
    def cost(self, x: float) -> None:
        self._cost = x


# noinspection PyAttributeOutsideInit
class EffectAssetInput(Asset):
    def __init__(self, ticker: str, name: str, ndf_code: str, spot_code: str, position_size: float) -> None:
        """EffectAsset class to hold data from database"""
        super().__init__(ticker)
        super().name = name
        self.ndf_code = ndf_code
        self.spot_code = spot_code
        self.position_size = position_size

    @property
    def ndf_code(self) -> str:
        return self._ndf_code

    @ndf_code.setter
    def ndf_code(self, x: str) -> None:
        self._ndf_code = x

    @property
    def spot_code(self) -> str:
        return self._spot_code

    @spot_code.setter
    def spot_code(self, x: str) -> None:
        self._spot_code = x

    @property
    def position_size(self) -> float:
        return self._position_size

    @position_size.setter
    def position_size(self, x: float) -> None:
        self._position_size = x
