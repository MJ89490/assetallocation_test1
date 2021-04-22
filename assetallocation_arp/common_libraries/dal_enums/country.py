from enum import Enum, auto


class Country(Enum):
    CN = auto()
    HK = auto()
    ID = auto()
    IN = auto()
    KR = auto()
    MY = auto()
    PH = auto()
    SG = auto()
    TH = auto()
    TW = auto()
    EG = auto()
    HU = auto()
    IL = auto()
    NG = auto()
    PL = auto()
    RO = auto()
    RU = auto()
    TR = auto()
    ZA = auto()
    CH = auto()
    CZ = auto()
    DE = auto()
    EU = auto()
    FR = auto()
    NO = auto()
    SE = auto()
    MULT = auto()
    JP = auto()
    AR = auto()
    BR = auto()
    CL = auto()
    CO = auto()
    MX = auto()
    PE = auto()
    CA = auto()
    US = auto()
    AU = auto()
    NZ = auto()
    GB = auto()
    EM = auto()
    IT = auto()
    SP = auto()


country_region = {
    'CN': 'Asia ex JP',
    'HK': 'Asia ex JP',
    'ID': 'Asia ex JP',
    'IN': 'Asia ex JP',
    'KR': 'Asia ex JP',
    'MY': 'Asia ex JP',
    'PH': 'Asia ex JP',
    'SG': 'Asia ex JP',
    'TH': 'Asia ex JP',
    'TW': 'Asia ex JP',
    'EG': 'CEEMEA',
    'HU': 'CEEMEA',
    'IL': 'CEEMEA',
    'NG': 'CEEMEA',
    'PL': 'CEEMEA',
    'RO': 'CEEMEA',
    'RU': 'CEEMEA',
    'TR': 'CEEMEA',
    'ZA': 'CEEMEA',
    'CH': 'Europe ex UK',
    'CZ': 'Europe ex UK',
    'DE': 'Europe ex UK',
    'EU': 'Europe ex UK',
    'FR': 'Europe ex UK',
    'NO': 'Europe ex UK',
    'SE': 'Europe ex UK',
    'MULT': 'Global',
    'JP': 'Japan',
    'AR': 'Latam',
    'BR': 'Latam',
    'CL': 'Latam',
    'CO': 'Latam',
    'MX': 'Latam',
    'PE': 'Latam',
    'CA': 'North America',
    'US': 'North America',
    'AU': 'Pacific',
    'NZ': 'Pacific',
    'GB': 'United Kingdom',
    'EM': 'EM',
    'IT': 'EU',
    'SP': 'EU'
}
