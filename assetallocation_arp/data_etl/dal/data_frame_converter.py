from typing import List

import pandas as pd

from assetallocation_arp.data_etl.dal.data_models.asset import Asset, TimesAssetInput


class DataFrameConverter:
    @staticmethod
    def assets_to_dataframe(assets: List[Asset]):
        # TODO find expected structure including analytics!
        pass

    @staticmethod
    def times_asset_inputs_to_dataframe(asset_inputs: List[TimesAssetInput]):
        # TODO implement this
        pass