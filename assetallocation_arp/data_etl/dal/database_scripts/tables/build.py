from pathlib import Path

from assetallocation_arp.data_etl.dal.database_scripts.build import execute_script_files


def create_tables(conn_str):
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

    execute_script_files(conn_str, files)


if __name__ == '__main__':
    from json import loads
    from os import environ

    config = loads(environ['DATABASE'])
    user = config['USER']
    password = config['PASSWORD']
    host = config['HOST']
    port = config['PORT']
    database = config['DATABASE']

    c_str = f'postgresql://{user}:{password}@{host}:{port}/{database}'
    create_tables(c_str)
