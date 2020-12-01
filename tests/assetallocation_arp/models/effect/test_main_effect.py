import os
import pandas as pd

from assetallocation_arp.models.effect.main_effect import run_effect

all_data = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "all_date.csv")), sep=',', engine='python')
all_data = all_data.set_index(pd.to_datetime(all_data.Date, format='%Y-%m-%d'))
del all_data['Date']

asset_inputs = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "all_asset_inputs.csv")), sep=',', engine='python')

strategy_inputs = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "strategy_inputs.csv")), sep=',', engine='python')

run_effect(strategy_inputs, asset_inputs, all_data)

