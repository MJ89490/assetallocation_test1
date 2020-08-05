from typing import Union

from assetallocation_arp.common_enums.currency import Currency


class Fund:
    def __init__(self, name: str, currency: Union[str, Currency]):
        self._name = name
        self.currency = currency

    @property
    def name(self):
        return self._name

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, x: Union[str, Currency]):
        self._currency = x if isinstance(x, Currency) else Currency[x]
