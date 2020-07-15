from .fundstrategy import FundStrategy
from .asset import Asset


class FundStrategyAssetWeight:
    def __init__(self, asset: Asset, fund_strategy: FundStrategy, fund_strategy_asset_weight_id: int,
                 implemented_weight: float, strategy_weight: float):
        self._asset = asset
        self._fund_strategy_run_id = fund_strategy
        self._id = fund_strategy_asset_weight_id
        self._implemented_weight = implemented_weight
        self._strategy_weight = strategy_weight
