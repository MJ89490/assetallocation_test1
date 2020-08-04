from decimal import Decimal

from assetallocation_arp.common_libraries.asset import Category
from assetallocation_arp.common_libraries.currency import Currency
from assetallocation_arp.common_libraries.country import Country, country_region
from assetallocation_arp.data_etl.dal.validate import validate_enum


# TODO rename type (+ enum?)
# TODO builder pattern for asset depending on times vs fica vs effect?
class Asset:
    def __init__(self, ticker: str, category: Category, country: Country, currency: Currency,
                 name: str, type: str):
        self.category = category
        self._cost = None
        self.country = country
        self.currency = currency
        self.description = ''
        self.future_ticker = ''
        self.generic_yield_ticker = ''
        self._name = name
        self.ndf_code = ''
        self._s_leverage = None
        self.signal_ticker = ''
        self.spot_code = ''
        self._ticker = ticker
        self.tr_flag = False
        self._type = type
        self._region = None

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, x: Category):
        validate_enum(x, Category.__members__.keys())
        self._category = x

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, x: Country):
        validate_enum(x, Country.__members__.keys())
        self._country = x
        self._region = country_region.get(x)

    @property
    def region(self):
        return self._region

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, x: str):
        self._group = x

    @property
    def s_leverage(self):
        return self._s_leverage

    @s_leverage.setter
    def s_leverage(self, x: int):
        self._s_leverage = x

    @property
    def ndf_code(self):
        return self._ndf_code

    @ndf_code.setter
    def ndf_code(self, x):
        self._ndf_code = x

    @property
    def future_ticker(self):
        return self._future_ticker

    @future_ticker.setter
    def future_ticker(self, x: str):
        self._future_ticker = x

    @property
    def generic_yield_ticker(self):
        return self._generic_yield_ticker

    @generic_yield_ticker.setter
    def generic_yield_ticker(self, x: str):
        self._generic_yield_ticker = x

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, x: Decimal):
        self._cost = x

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, x: Currency):
        validate_enum(x, Currency.__members__.keys())
        self._currency = x

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
    def signal_ticker(self):
        return self._signal_ticker

    @signal_ticker.setter
    def signal_ticker(self, x: str):
        self._signal_ticker = x

    @property
    def spot_code(self):
        return self._spot_code

    @spot_code.setter
    def spot_code(self, x: str):
        self._spot_code = x

    @property
    def tr_flag(self):
        return self._tr_flag

    @tr_flag.setter
    def tr_flag(self, x: bool):
        self._tr_flag = x
