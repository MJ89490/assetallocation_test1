from assetallocation_arp.common_libraries.currency import Currency
from assetallocation_arp.data_etl.dal.validate import validate_enum


class Fund:
    def __init__(self, name: str, currency: Currency):
        self._name = name
        self.currency = currency

    @property
    def name(self):
        return self._name

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, x: Currency):
        validate_enum(x, Currency.__members__.keys())
        self._currency = x
