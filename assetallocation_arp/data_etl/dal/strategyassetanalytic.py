from .fundstrategy import FundStrategy
from .asset import Asset


class StrategyAssetAnalytic:
    def __init__(self, asset: Asset, fund_strategy: FundStrategy, strategy_asset_analytic_id: int,
                 strategy_asset_analytic_sub_type: str, strategy_asset_analytic_type: str, value: float):
        self._asset = asset
        self._fund_strategy_run_id = fund_strategy
        self._id = strategy_asset_analytic_id
        self._sub_type = strategy_asset_analytic_sub_type
        self._strategy_asset_analytic_type = strategy_asset_analytic_type
        self._value = value
