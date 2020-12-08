from enum import Enum, auto


# TODO use enums in Effect UI inputs dropdown
TrendIndicator = Enum(
    value='TrendIndicator',
    names=[
        ('total return', auto()),
        ('spot', auto()),
    ]
)

# noinspection PyArgumentList
RiskWeighting = Enum(
    value='RiskWeighting',
    names=[
        ('1/N', auto()),
        ('inverse vol', auto()),
        ('inverse carry', auto())
    ]
)


class CarryType(Enum):
    nominal = auto()
    real = auto()


class Frequency(Enum):
    monthly = auto()
    weekly = auto()
    daily = auto()


class DayOfWeek(Enum):
    MON = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6


class Leverage(Enum):
    e = auto()   # Equal(e)
    n = auto()   # Normative(n)
    v = auto()   # Volatility(v)
    s = auto()   # Standalone(s)


class Name(Enum):
    times = auto()
    maven = auto()
    effect = auto()
    curp = auto()
    fica = auto()
    factor = auto()
    comca = auto()
    fx = auto()


# noinspection PyArgumentList
FxModel = Enum(
    value='Performance',
    names=[
        ('cumo', auto()),
        ('cuca', auto()),
        ('curp', auto()),
        ('dyn hdge', auto()),
        ('ppp all', auto()),
        ('ppp usd', auto()),
        ('ppp curp', auto())
    ]
)
