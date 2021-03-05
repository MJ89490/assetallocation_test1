from pathlib import Path
from typing import List


def get_table_sql_files() -> List[str]:
    """Return ordered list of sql files required to build tables"""
    p = Path(__file__).parent
    a = p / 'asset'
    ar = p / 'arp'
    au = p / 'audit'
    co = p / 'config'
    f = p / 'fund'
    lo = p / 'lookup'
    s = p / 'staging'

    files = [lo / 'country.sql', lo / 'currency.sql', lo / 'source.sql', co / 'execution.sql',
             co / 'execution_state.sql', co / 'model.sql', co / 'model_instance.sql',
             f / 'fund.sql', au / 'logged_action.sql', a / 'asset_group.sql', a / 'asset.sql', a / 'asset_analytic.sql',
             ar / 'app_user.sql', ar / 'strategy.sql', ar / 'effect.sql', ar / 'fica.sql', ar / 'times.sql',
             ar / 'fx.sql', ar / 'maven.sql', ar / 'strategy_asset_group.sql', ar / 'effect_asset_group.sql',
             ar / 'times_asset_group.sql', ar / 'fx_asset_group.sql', ar / 'maven_asset_group.sql',
             ar / 'strategy_asset.sql', ar / 'strategy_asset_analytic.sql', ar / 'strategy_analytic.sql',
             ar / 'strategy_asset_weight.sql', ar / 'fund_strategy_asset_weight.sql', ar / 'fund_strategy_weight.sql',
             s / 'asset.sql']

    return files
