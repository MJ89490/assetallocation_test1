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
