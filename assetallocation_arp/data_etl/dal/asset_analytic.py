from decimal import Decimal

from assetallocation_arp.data_etl.dal.source import Source


# TODO add enum for asset_analytic_type
class AssetAnalytic:
    def __init__(self, source: Source, type: str, value: Decimal):
        self._source = source
        self._type = type
        self._value = value
