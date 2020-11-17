from enum import Enum, auto


class Category(Enum):
    sovereign = auto()
    swap = auto()
    swap_cr = auto()
    future = auto()


class CurveTenor(Enum):
    mth3 = auto()
    yr1 = auto()
    yr2 = auto()
    yr3 = auto()
    yr4 = auto()
    yr5 = auto()
    yr6 = auto()
    yr7 = auto()
    yr8 = auto()
    yr9 = auto()
    yr10 = auto()
    yr15 = auto()
    yr20 = auto()
    yr30 = auto()
