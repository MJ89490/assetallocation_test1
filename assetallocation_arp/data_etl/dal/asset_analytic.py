from decimal import Decimal

from .source import Source


class AssetAnalytic:
    def __init__(self, source: Source, asset_analytic_type: str, value: Decimal):
        self._source = source
        self._type = asset_analytic_type
        self._value = value

