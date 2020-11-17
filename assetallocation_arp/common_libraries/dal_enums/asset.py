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
    AUD = auto()
    CAD = auto()
    CHF = auto()
    EUR = auto()
    GBP = auto()
    JPY = auto()
    NOK = auto()
    NZD = auto()
    SEK = auto()
    USD = auto()
    EURGBP = auto()  # TODO check this is FX not commodity or credit



# noinspection PyArgumentList
EQ = Subcategory(
    value='EQ',
    names=[
        ('USD (EQ)', auto()),
        ('GBP (EQ)', auto()),
        ('EUR (EQ)', auto()),
        ('JPY (EQ)', auto()),
        ('CAD (EQ)', auto()),
        ('AUD (EQ)', auto()),
        ('SEK (EQ)', auto()),
        ('CHF (EQ)', auto()),
        ('EMG (EQ)', auto()),
        ('EU_SC (EQ)', auto()),
        ('US_SC (EQ)', auto()),
        ('UK_SC (EQ)', auto()),
    ]
)

# noinspection PyArgumentList
FI = Subcategory(
    value='FI',
    names=[
        ('USD (FI)', auto()),
        ('GBP (FI)', auto()),
        ('EUR (FI)', auto()),
        ('JPY (FI)', auto()),
        ('CAD (FI)', auto()),
        ('AUD (FI)', auto()),
        ('PERIPH (FI)', auto()),
    ]
)

# noinspection PyArgumentList
COM = Subcategory(
    value='COM',
    names=[
        ('BROAD(COM)', auto()),
    ]
)

# noinspection PyArgumentList
CRED = Subcategory(
    value='CRED',
    names=[
        ('HY US (CRED)', auto()),
        ('IG US (CRED)', auto()),
        ('EMBI (CRED)', auto()),
        ('IG EU (CRED)', auto()),
        ('HY EU (CRED)', auto()),
        ('GBI (CRED)', auto()),
        ('IG UK (CRED)', auto()),
    ]
)

# noinspection PyArgumentList
RE = Subcategory(
    value='RE',
    names=[
        ('US (RE)', auto()),
        ('EU (RE)', auto()),
        ('AS (RE)', auto()),
        ('UK (RE)', auto()),
    ]
)

# noinspection PyArgumentList
TIPS = Subcategory(
    value='TIPS',
    names=[
        ('US (TIPS)', auto()),
        ('EU (TIPS)', auto()),
        ('UK (TIPS)', auto()),
    ]
)

# noinspection PyArgumentList
CASH = Subcategory(
    value='CASH',
    names=[
        ('AUD (CASH)', auto()),
        ('CAD (CASH)', auto()),
        ('CHF (CASH)', auto()),
        ('GBP (CASH)', auto()),
        ('EUR (CASH)', auto()),
        ('JPY (CASH)', auto()),
        ('SEK (CASH)', auto()),
        ('USD (CASH)', auto()),
    ]
)

subcategory_map = {j: i[j] for i in (Equity, FixedIncome, FX, EQ, FI, COM, CRED, RE, TIPS, CASH) for j in i._member_names_}

















