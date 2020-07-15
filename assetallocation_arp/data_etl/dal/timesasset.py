from .asset import Asset
from .times import Times


class TimesAsset:
    def __init__(self, asset: Asset, times_asset_id: int, strategy: Times):
        self._asset = asset
        self._times_asset_id = times_asset_id
        self._strategy = strategy
