from decimal import Decimal
from abc import ABC
from typing import List, Union

from assetallocation_arp.common_enums.asset import Category
from assetallocation_arp.common_enums.currency import Currency
from assetallocation_arp.common_enums.country import Country, country_region
from assetallocation_arp.data_etl.dal.asset_analytic import AssetAnalytic


# TODO rename type (+ enum?)
class Asset(ABC):
    def __init__(self, ticker: str, category: Union[str, Category], country: Union[str, Country],
                 currency: Union[str, Currency], name: str, type: str):
        self.category = category
        self.country = country
        self.currency = currency
        self.description = ''
        self._name = name
        self._ticker = ticker
        self.tr_flag = False
        self._type = type
        self._region = None
        self._asset_analytics = []

    @property
    def asset_analytics(self):
        return self._asset_analytics

    @asset_analytics.setter
    def asset_analytics(self, x: List[AssetAnalytic]):
        self._asset_analytics = x

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, x: Union[str, Category]):
        self._category = x if isinstance(x, Category) else Category[x]

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, x: Union[str, Country]):
        self._country = x if isinstance(x, Country) else Country[x]
        self._region = country_region.get(x.name)

    @property
    def region(self):
        return self._region

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, x: str):
        self._type = x

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, x: Union[str, Currency]):
        self._currency = x if isinstance(x, Currency) else Currency[x]

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, x: str):
        self._description = x

    @property
    def ticker(self):
        return self._ticker

    @property
    def tr_flag(self):
        return self._tr_flag

    @tr_flag.setter
    def tr_flag(self, x: bool):
        self._tr_flag = x

    def add_analytic(self, asset_analytic: AssetAnalytic):
        if asset_analytic.asset_ticker == self.ticker:
            self._asset_analytics.append(asset_analytic)
        else:
            raise ValueError(f'Tickers do not match. Asset ticker is "{self.ticker}"'
                             f'but asset_analytic has a ticker of "{asset_analytic.ticker}"')


class FicaAsset(Asset):
    def __init__(self, ticker: str, category: Category, country: Country, currency: Currency, name: str, type: str,
                 future_ticker: str, generic_yield_ticker: str):
        super().__init__(ticker, category, country, currency, name, type)
        self._future_ticker = future_ticker
        self._generic_yield_ticker = generic_yield_ticker

    @property
    def generic_yield_ticker(self):
        return self._generic_yield_ticker

    @generic_yield_ticker.setter
    def generic_yield_ticker(self, x: str):
        self._generic_yield_ticker = x


class TimesAsset(Asset):
    def __init__(self, ticker: str, category: Category, country: Country, currency: Currency, name: str, type: str,
                 s_leverage: int, signal_ticker: str, future_ticker: str, cost: Decimal):
        super().__init__(ticker, category, country, currency, name, type)
        self.signal_ticker = signal_ticker
        self.future_ticker = future_ticker
        self.cost = cost
        self.s_leverage = s_leverage

    @property
    def s_leverage(self):
        return self._s_leverage

    @s_leverage.setter
    def s_leverage(self, x: int):
        self._s_leverage = x

    @property
    def signal_ticker(self):
        return self._signal_ticker

    @signal_ticker.setter
    def signal_ticker(self, x: str):
        self._signal_ticker = x

    @property
    def future_ticker(self):
        return self._future_ticker

    @future_ticker.setter
    def future_ticker(self, x: str):
        self._future_ticker = x

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, x: Decimal):
        self._cost = x


class EffectAsset(Asset):
    def __init__(self, ticker: str, category: Category, country: Country, currency: Currency, name: str, type: str,
                 ndf_code: str, spot_code: str, position_size: Decimal):
        super().__init__(ticker, category, country, currency, name, type)
        self.ndf_code = ndf_code
        self.spot_code = spot_code
        self.position_size = position_size

    @property
    def ndf_code(self):
        return self._ndf_code

    @ndf_code.setter
    def ndf_code(self, x):
        self._ndf_code = x

    @property
    def spot_code(self):
        return self._spot_code

    @spot_code.setter
    def spot_code(self, x: str):
        self._spot_code = x

    @property
    def position_size(self):
        return self._position_size

    @position_size.setter
    def position_size(self, x: Decimal):
        self._position_size = x
