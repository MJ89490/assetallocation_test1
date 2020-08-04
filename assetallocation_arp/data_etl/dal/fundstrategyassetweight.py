from decimal import Decimal


class FundStrategyAssetWeight:
    def __init__(self, asset_ticker: str, strategy_weight: Decimal):
        self._asset_ticker = asset_ticker
        self._strategy_weight = strategy_weight
        self._implemented_weight = 0

    @property
    def implemented_weight(self):
        return self._implemented_weight

    @implemented_weight.setter
    def implemented_weight(self, x: Decimal):
        self._implemented_weight = x

    @property
    def strategy_weight(self):
        return self._strategy_weight

    @strategy_weight.setter
    def strategy_weight(self, x):
        self._strategy_weight = x

    @property
    def asset_ticker(self):
        return self._asset_ticker

    @asset_ticker.setter
    def asset_ticker(self, x):
        self._asset_ticker = x