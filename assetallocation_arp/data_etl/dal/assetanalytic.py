from psycopg2.extras import DateTimeTZRange

from .asset import Asset
from .source import Source

class AssetAnalytic:
    def __init__(self, asset: Asset, business_tstzrange: DateTimeTZRange, asset_analytic_id: int, source: Source,
                 system_tstzrange: DateTimeTZRange, asset_analytic_type: str, value: float):
        self._asset = asset
        self._business_tstzrange = business_tstzrange
        self._id = asset_analytic_id
        self._source = source
        self._system_tstzrange = system_tstzrange
        # enumeration
        self._type = asset_analytic_type
        self._value = value

