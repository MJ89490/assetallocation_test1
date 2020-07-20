from .asset import Asset
from .times import Times


class TimesAsset:
    def __init__(self, asset: Asset, strategy: Times):
        self._asset = asset
        self._strategy = strategy
