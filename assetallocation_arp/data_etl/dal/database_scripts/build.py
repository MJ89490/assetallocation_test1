from sqlalchemy import text


from assetallocation_arp.data_etl.dal.database_scripts.schemas.build import get_schema_sql_files
from assetallocation_arp.data_etl.dal.database_scripts.types.build import get_type_sql_files
from assetallocation_arp.data_etl.dal.database_scripts.tables.build import get_table_sql_files
from assetallocation_arp.data_etl.dal.database_scripts.functions.build import get_function_sql_files
from assetallocation_arp.data_etl.dal.database_scripts.static_data.build import get_static_data_sql_files
from assetallocation_arp.data_etl.dal.database_scripts.triggers.build import get_trigger_sql_files


def execute_script_files(engine, files) -> None:
    """Read sql from file and execute against database"""
    conn = engine.connect()

    for filename in files:
        with open(filename, 'r') as f:
            sql_file = f.read()

        try:
            conn.execute(text(sql_file))
        except Exception as e:
            print(filename)
            print(e)

    conn.close()


def create_all(engine) -> None:
    """Create schemas, types, tables, functions, static data and triggers in database"""
    sql_files = []
    sql_files.extend(get_schema_sql_files())
    sql_files.extend(get_type_sql_files())
    sql_files.extend(get_table_sql_files())
    sql_files.extend(get_function_sql_files())  # TODO fix audit functions not working
    sql_files.extend(get_static_data_sql_files())
    sql_files.extend(get_trigger_sql_files())

    execute_script_files(engine, sql_files)


if __name__ == '__main__':
    from json import loads
    from os import environ

    from sqlalchemy import create_engine

    config = loads(environ['DATABASE'])
    user = config['USER']
    password = config['PASSWORD']
    host = config['HOST']
    port = config['PORT']
    database = config['DATABASE']

    c_str = f'postgresql://{user}:{password}@{host}:{port}/{database}'
    en = create_engine(c_str)
    create_all(en)