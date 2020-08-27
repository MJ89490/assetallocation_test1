from enum import Enum, auto


# noinspection PyArgumentList
Category = Enum(
    value='Category',
    names=[
        ('Equity', auto()),
        ('Fixed Income', auto()),
        ('FX', auto()),
        ('Commodity', auto()),
        ('Credit', auto())
    ]
)


class Equity(Enum):
    US_Equities = auto()
    EU_Equities = auto()
    JP_Equities = auto()
    HK_Equities = auto()


class FixedIncome(Enum):
    US_10_y_Bonds = auto()
    UK_10_y_Bonds = auto()
    EU_10_y_Bonds = auto()
    CA_10_y_Bonds = auto()


class FX(Enum):
    JPY = auto()
    EUR = auto()
    AUD = auto()
    CAD = auto()
    GBP = auto()
