from .asset import Asset
from .fica import Fica
from .ticker import Ticker


class FicaAsset:
    def __init__(self, asset: Asset, cr_swap_ticker: Ticker, fica_asset_id: int, sovereign_ticker: Ticker,
                 strategy: Fica, swap_ticker: Ticker):
        self.asset_id = asset
        self.cr_swap_ticker_id = cr_swap_ticker
        self._id = fica_asset_id
        self._sovereign_ticker_id = sovereign_ticker
        self._strategy_id = strategy
        self._swap_ticker_id = swap_ticker
