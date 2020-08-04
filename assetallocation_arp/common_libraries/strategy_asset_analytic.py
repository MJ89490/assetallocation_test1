from enum import Enum, auto


class Category(Enum):
    performance = auto()
    signal = auto()


Performance = Enum(
    value='Performance',
    names=[
        ('carry', auto()),
        ('signal', auto()),
        ('FX', auto()),
        ('total return', auto()),
        ('excess return', auto())
    ]
)


class Signal(Enum):
    carry = auto()
    momentum = auto()
    value = auto()
