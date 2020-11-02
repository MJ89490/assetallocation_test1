from enum import Enum, auto


class TrendIndicator(Enum):
    TotalReturn = auto()
    Spot = auto()


class CarryType(Enum):
    Nominal = auto()
    Real = auto()


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
    fxmodels = auto()
