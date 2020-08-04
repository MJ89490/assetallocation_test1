from typing import List

from assetallocation_arp.data_etl.dal.asset import Asset
from assetallocation_arp.data_etl.dal.times import Times


class TimesAsset:
    def __init__(self, strategy: Times, assets: List[Asset]):
        self._strategy = strategy
        self._assets = assets
