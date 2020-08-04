from decimal import Decimal
from datetime import datetime
from typing import List

from assetallocation_arp.common_libraries.models_names import Models
from assetallocation_arp.data_etl.dal.validate import validate_enum
from assetallocation_arp.data_etl.dal.strategyassetanalytic import StrategyAssetAnalytic
from assetallocation_arp.data_etl.dal.fundstrategyassetweight import FundStrategyAssetWeight


class FundStrategy:
    def __init__(self, fund_name: str, strategy_name: Models, strategy_version: int, weight: Decimal,
                 strategy_asset_analytics: List[StrategyAssetAnalytic],
                 fund_strategy_asset_weights: List[FundStrategyAssetWeight]):
        self._fund_name = fund_name
        self._strategy_name = strategy_name
        self._weight = weight
        self._output_is_saved = True
        self._business_datetime = datetime.now()
        self._python_code_version = '0'  # TODO set this somewhere to use code wide
        self._strategy_version = strategy_version
        self._fund_strategy_asset_weights = fund_strategy_asset_weights
        self._strategy_asset_analytics = strategy_asset_analytics

    @property
    def strategy_name(self):
        return self._strategy_name

    @strategy_name.setter
    def strategy_name(self, x):
        validate_enum(x, Models.__members__.keys())
        self._strategy_name = x

    @property
    def strategy_version(self):
        return self._strategy_version

    @strategy_version.setter
    def strategy_version(self, x: int):
        self._strategy_version = x

    @property
    def business_datetime(self):
        return self._business_datetime

    @business_datetime.setter
    def business_datetime(self, x: datetime):
        self._business_datetime = x

    @property
    def output_is_saved(self):
        return self._output_is_saved

    @output_is_saved.setter
    def output_is_saved(self, x: bool):
        self._output_is_saved = x

    @property
    def weight(self):
        return self._weight
