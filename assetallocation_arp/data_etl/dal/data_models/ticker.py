from typing import Union

from assetallocation_arp.common_libraries.dal_enums import curve


# noinspection PyAttributeOutsideInit
class Ticker:
    def __init__(self, category: str, mth3: str, yr1: str, yr2: str, yr3: str, yr4: str, yr5: str, yr6: str, yr7: str,
                 yr8: str, yr9: str, yr10: str, yr15: str, yr20: str, yr30: str):
        """Ticker class to hold data from database"""
        self.category = category
        self._mth3 = mth3
        self._yr1 = yr1
        self._yr2 = yr2
        self._yr3 = yr3
        self._yr4 = yr4
        self._yr5 = yr5
        self._yr6 = yr6
        self._yr7 = yr7
        self._yr8 = yr8
        self._yr9 = yr9
        self._yr10 = yr10
        self._yr15 = yr15
        self._yr20 = yr20
        self._yr30 = yr30

    @property
    def category(self) -> curve.Category:
        return self._category

    @category.setter
    def category(self, x: Union[curve.Category, str]) -> None:
        self._category = x if isinstance(x, curve.Category) else curve.Category[x]

    @property
    def mth3(self) -> str:
        return self._mth3

    @mth3.setter
    def mth3(self, x: str) -> None:
        self._mth3 = x

    @property
    def yr10(self) -> str:
        return self._yr10 
        
    @yr10.setter
    def yr10(self, x: str) -> None:
        self._yr10 = x

    @property
    def yr1(self) -> str:
        return self._yr1 
        
    @yr1.setter
    def yr1(self, x: str) -> None:
        self._yr1 = x

    @property
    def yr2(self) -> str:
        return self._yr2 
        
    @yr2.setter
    def yr2(self, x: str) -> None:
        self._yr2 = x

    @property
    def yr3(self) -> str:
        return self._yr3 
        
    @yr3.setter
    def yr3(self, x: str) -> None:
        self._yr3 = x

    @property
    def yr4(self) -> str:
        return self._yr4 
        
    @yr4.setter
    def yr4(self, x: str) -> None:
        self._yr4 = x

    @property
    def yr5(self) -> str:
        return self._yr5 
        
    @yr5.setter
    def yr5(self, x: str) -> None:
        self._yr5 = x

    @property
    def yr6(self) -> str:
        return self._yr6 
        
    @yr6.setter
    def yr6(self, x: str) -> None:
        self._yr6 = x

    @property
    def yr7(self) -> str:
        return self._yr7 
        
    @yr7.setter
    def yr7(self, x: str) -> None:
        self._yr7 = x

    @property
    def yr8(self) -> str:
        return self._yr8 
        
    @yr8.setter
    def yr8(self, x: str) -> None:
        self._yr8 = x

    @property
    def yr9(self) -> str:
        return self._yr9 
        
    @yr9.setter
    def yr9(self, x: str) -> None:
        self._yr9 = x

    @property
    def yr10(self) -> str:
        return self._yr10 
        
    @yr10.setter
    def yr10(self, x: str) -> None:
        self._yr10 = x
        
    @property
    def yr15(self) -> str:
        return self._yr15 
        
    @yr15.setter
    def yr15(self, x: str) -> None:
        self._yr15 = x

    @property
    def yr20(self) -> str:
        return self._yr20 
        
    @yr20.setter
    def yr20(self, x: str) -> None:
        self._yr20 = x

    @property
    def yr30(self) -> str:
        return self._yr30
        
    @yr30.setter
    def yr30(self, x: str) -> None:
        self._yr30 = x
