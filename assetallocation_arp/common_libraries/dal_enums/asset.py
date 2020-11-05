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


class Subcategory(Enum):
    pass


# noinspection PyArgumentList
Equity = Subcategory(
    value='Equity',
    names=[
        ('US Equities', auto()),
        ('EU Equities', auto()),
        ('JP Equities', auto()),
        ('HK Equities', auto()),
    ]
)

# noinspection PyArgumentList
FixedIncome = Subcategory(
    value='FixedIncome',
    names=[
        ('US 10y Bonds', auto()),
        ('UK 10y Bonds', auto()),
        ('EU 10y Bonds', auto()),
        ('CA 10y Bonds', auto()),
    ]
)


class FX(Subcategory):
    JPY = auto()
    EUR = auto()
    AUD = auto()
    CAD = auto()
    GBP = auto()
    EURGBP = auto()  # TODO check this is FX not commodity or credit


subcategory_map = {j: i for i in (Equity, FixedIncome, FX) for j in i._member_names_}
