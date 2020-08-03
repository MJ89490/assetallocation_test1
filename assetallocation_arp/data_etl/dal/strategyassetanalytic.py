from decimal import Decimal


class StrategyAssetAnalytic:
    def __init__(self, asset_ticker: str, analytic_type: str,
                 analytic_sub_type: str, value: Decimal):
        self._asset_ticker = asset_ticker
        self._analytic_type = analytic_type
        self._analytic_subtype = analytic_sub_type
        self._value = value

    @property
    def asset_ticker(self):
        return self._asset_ticker

    @property
    def analytic_type(self):
        return self._analytic_type

    @property
    def analytic_subtype(self):
        return self._analytic_subtype

    @property
    def value(self):
        return self._value
