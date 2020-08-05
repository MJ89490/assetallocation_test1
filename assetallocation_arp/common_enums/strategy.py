from enum import Enum, auto


class TrendIndicator(Enum):
    TotalReturn = auto()
    Spot = auto()


class CarryType(Enum):
    Nominal = auto()
    Real = auto()


class Frequency(Enum):
    monthly = 0
    weekly = 1
    daily = 2


class DayOfWeek(Enum):
    MON = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6


class Leverage(Enum):
    e = 0   #Equal(e)
    n = 1   #Normative(n)
    v = 2   #Volatility(v)
    s = 3   #Standalone(s)


class Name(Enum):
    times = 0
    maven = 1
    effect = 2
    curp = 3
    fica = 4
    factor = 5
    comca = 6
