from decimal import Decimal


class FundStrategyAssetWeight:
    def __init__(self, asset_ticker: str, implemented_weight: Decimal, strategy_weight: Decimal):
        self._asset_ticker = asset_ticker
        self._implemented_weight = implemented_weight
        self._strategy_weight = strategy_weight

    @property
    def asset_ticker(self):
        return self._asset_ticker

    @property
    def implemented_weight(self):
        return self._implemented_weight

    @property
    def strategy_weight(self):
        return self._strategy_weight
