from .asset import Asset
from .effect import Effect


class EffectAsset:
    def __init__(self, asset: Asset, effect_asset_id: int, position_size: float, strategy: Effect):
        self._asset = asset
        self._id = effect_asset_id
        self._position_size = position_size
        self._strategy = strategy
