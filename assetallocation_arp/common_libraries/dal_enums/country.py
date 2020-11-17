from enum import Enum, auto


# TODO update in DB
class Country(Enum):
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


# TODO update the below ask SIMONE
country_region = {
    'USD': 'North America',
    'EUR': 'Europe',
    'JPY': 'Asia'
}
