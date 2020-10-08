from typing import Union

from assetallocation_arp.common_libraries.dal_enums.curve import Category


# noinspection PyAttributeOutsideInit
class Ticker:
    def __init__(self, yr10: str, yr15: str, yr1: str, yr20: str, yr2: str,
                 yr30: str, mth3: str, yr3: str, yr4: str, yr5: str, yr6: str,
                 yr7: str, yr8: str, yr9: str, category: str):
        """Ticker class to hold data from database"""
        self._yr10 = yr10
        self._yr15 = yr15
        self._yr1 = yr1
        self._yr20 = yr20
        self._yr2 = yr2
        self._yr30 = yr30
        self._mth3 = mth3
        self._yr3 = yr3
        self._yr4 = yr4
        self._yr5 = yr5
        self._yr6 = yr6
        self._yr7 = yr7
        self._yr8 = yr8
        self._yr9 = yr9
        self.category = category

    @property
    def category(self) -> Category:
        return self._category

    @category.setter
    def category(self, x: Union[Category, str]) -> None:
        self._category = x if isinstance(x, Category) else Category[x]
