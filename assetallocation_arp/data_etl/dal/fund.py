from assetallocation_arp.common_enums.currency import Currency
from assetallocation_arp.data_etl.dal.validate import check_value


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
        check_value(x, Currency.__members__.keys())
        self._currency = x
