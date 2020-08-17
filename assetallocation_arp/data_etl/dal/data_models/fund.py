from typing import Union

from assetallocation_arp.common_enums.currency import Currency


# noinspection PyAttributeOutsideInit
class Fund:
    def __init__(self, name: str, currency: Union[str, Currency]) -> None:
        """Fund class to hold data from database"""
        self._name = name
        self.currency = currency

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, x: str) -> None:
        self._name = x

    @property
    def currency(self) -> Currency:
        return self._currency

    @currency.setter
    def currency(self, x: Union[str, Currency]) -> None:
        self._currency = x if isinstance(x, Currency) else Currency[x]
