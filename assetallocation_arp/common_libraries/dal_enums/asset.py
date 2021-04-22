from enum import Enum, auto


# noinspection PyArgumentList
Category = Enum(
    value='Category',
    names=[
        ('Equity', auto()),
        ('Fixed Income', auto()),
        ('FX', auto()),
        ('Commodity', auto()),
        ('Indicator', auto())
    ]
)


class Subcategory(Enum):
    pass


# noinspection PyArgumentList
Equity = Subcategory(
    value='Equity',
    names=[
        ('REITS', auto()),
        ('Equity Factor', auto()),
        ('Small Cap Equity', auto()),
        ('DM Equity', auto()),
        ('Equity Sector', auto()),
        ('EM Equity', auto()),
    ]
)

# noinspection PyArgumentList
FixedIncome = Subcategory(
    value='FixedIncome',
    names=[
        ('EM Debt Local', auto()),
        ('EM Debt Hard', auto()),
        ('Nominal Swap', auto()),
        ('IL Bond', auto()),
        ('Nominal Bond', auto()),
        ('Credit', auto()),
    ]
)

# noinspection PyArgumentList
FX = Subcategory(
    value='FX',
    names=[
        ('DM FX', auto()),
        ('EM FX', auto())
    ]
)

# noinspection PyArgumentList
Commodity = Subcategory(
    value='Commodity',
    names=[
        ('Natgas', auto()),
        ('Industrial Metals', auto()),
        ('Energy', auto()),
        ('Agriculture', auto()),
        ('Precious Metals', auto()),
        ('Commodity', auto()),
    ]
)

# noinspection PyArgumentList
Indicator = Subcategory(
    value='Indicator',
    names=[
        ('IMF Inflation Expectation', auto()),
        ('OECD PPP', auto())
    ]
)

subcategory_map = {
    subcategory: category[subcategory]
    for category in (Equity, FixedIncome, FX, Commodity, Indicator)
    for subcategory in category._member_names_
}
