from sqlalchemy import create_engine
from pathlib import Path


def execute_scripts_from_file(filename, conn):
    with open(filename, 'r') as f:
        sql_file = f.read()

    sql_commands = sql_file.split(';')
    sql_commands = filter(lambda x: x != '', sql_commands)

    for c in sql_commands:
        try:
            conn.execute(c)
        except Exception as e:
            print(filename)
            print(e)


def main():
    p = Path(__file__).parent
    a = p / 'asset'
    ar = p / 'arp'
    au = p / 'audit'
    co = p / 'config'
    cu = p / 'curve'
    f = p / 'fund'
    l = p / 'lookup'

    files = [p / 'schema.sql', l / 'country.sql', l / 'currency.sql', l / 'source.sql', co / 'execution.sql',
             co / 'execution_state.sql', cu / 'ticker.sql', f / 'fund.sql', au / 'logged_action.sql', a / 'asset.sql',
             a / 'asset_analytic.sql', ar / 'app_user.sql', ar / 'strategy.sql', ar / 'effect.sql', ar / 'fica.sql',
             ar / 'times.sql', ar / 'effect_asset.sql', ar / 'fica_asset.sql', ar / 'times_asset.sql',
             ar / 'fund_strategy.sql', ar / 'fund_strategy_asset_weight.sql', ar / 'fund_strategy_asset_analytic.sql']

    c_str = 'postgresql://d00_asset_allocation_data_migration:changeme@n00-pgsql-nexus-businessstore-writer.inv.adroot.lgim.com:54323/d00_asset_allocation_data'
    engine = create_engine(c_str, echo=True)
    conn = engine.connect()

    for filename in files:
        execute_scripts_from_file(filename, conn)


if __name__ == '__main__':
    main()
