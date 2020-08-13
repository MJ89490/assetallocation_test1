from pathlib import Path


def get_table_sql_files():
    p = Path(__file__).parent
    a = p / 'asset'
    ar = p / 'arp'
    au = p / 'audit'
    co = p / 'config'
    cu = p / 'curve'
    f = p / 'fund'
    lo = p / 'lookup'

    files = [lo / 'country.sql', lo / 'currency.sql', lo / 'source.sql', co / 'execution.sql',
             co / 'execution_state.sql', cu / 'ticker.sql', f / 'fund.sql', au / 'logged_action.sql', a / 'asset.sql',
             a / 'asset_analytic.sql', ar / 'app_user.sql', ar / 'strategy.sql', ar / 'effect.sql', ar / 'fica.sql',
             ar / 'times.sql', ar / 'effect_asset.sql', ar / 'fica_asset.sql', ar / 'times_asset.sql',
             ar / 'fund_strategy.sql', ar / 'fund_strategy_asset_weight.sql', ar / 'fund_strategy_asset_analytic.sql']

    return files
