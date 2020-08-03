from .country import Country
from .currency import Currency


class Asset:
    def __init__(self, asset_class: str, cost: float, country: Country, currency: Currency, description: str,
                 future_ticker: str, generic_yield_ticker: str, name: str, ndf_code: str, s_leverage: int,
                 signal_ticker: str, spot_code: str, ticker: int, tr_flag: bool, asset_type: str):
        self._asset_class = asset_class
        self._cost = cost
        self._country = country
        self._currency = currency
        self._description = description
        self._future_ticker = future_ticker
        self._generic_yield_ticker = generic_yield_ticker
        self._name = name
        self._ndf_code = ndf_code
        self._s_leverage = s_leverage
        self._signal_ticker = signal_ticker
        self._spot_code = spot_code
        self._ticker = ticker
        self._tr_flag = tr_flag
        self._type = asset_type
