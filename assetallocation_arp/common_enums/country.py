from enum import Enum, auto


class Country(Enum):
    US = auto()
    EU = auto()
    JP = auto()


country_region = {
    'US': 'North America',
    'EU': 'Europe',
    'JP': 'Asia'
}
