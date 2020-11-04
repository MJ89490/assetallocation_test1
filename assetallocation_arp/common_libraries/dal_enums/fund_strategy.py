from enum import Enum, auto


class Category(Enum):
    performance = auto()
    signal = auto()


# noinspection PyArgumentList
Performance = Enum(
    value='Performance',
    names=[
        ('carry', auto()),
        ('spot', auto()),
        ('beta', auto()),
        ('correlation', auto()),
        ('total return', auto()),
        ('excess return', auto()),
        ('excess return index', auto()),
        ('total return index', auto())
    ]
)


Signal = Enum(
    value='Signal',
    names=[
        ('carry', auto()),
        ('momentum', auto()),
        ('value', auto()),
        ('signal strength', auto()),
    ]
)


class AggregationLevel(Enum):
    asset = auto()
    strategy = auto()
    comparator = auto()
