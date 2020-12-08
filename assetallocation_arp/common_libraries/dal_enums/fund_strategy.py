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
        ('total return index', auto()),
        ('total return index incl signals', auto()),
        ('total return index excl signals', auto()),
        ('spot index incl signals', auto()),
        ('spot index excl signals', auto())
    ]
)
# TODO add NEW in database accepted (or remove enum / check from database)


Signal = Enum(
    value='Signal',
    names=[
        ('carry', auto()),
        ('momentum', auto()),
        ('value', auto()),
        ('signal strength', auto()),
        ('trend', auto()),
    ]
)
# TODO add 'trend' in database accepted (or remove enum / check from database)

class AggregationLevel(Enum):
    asset = auto()
    strategy = auto()
    comparator = auto()
