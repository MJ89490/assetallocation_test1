from sqlalchemy import text, create_engine


def execute_script_files(conn_str, files):
    engine = create_engine(conn_str, echo=False)
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


# Imported after execute_script_files to avoid circular imports
from assetallocation_arp.data_etl.dal.database_scripts.schemas.build import create_schemas
from assetallocation_arp.data_etl.dal.database_scripts.types.build import create_types
from assetallocation_arp.data_etl.dal.database_scripts.tables.build import create_tables
from assetallocation_arp.data_etl.dal.database_scripts.functions.build import create_functions
from assetallocation_arp.data_etl.dal.database_scripts.static_data.build import insert_static_data


def create_all(conn_str):
    create_schemas(conn_str)
    create_types(conn_str)
    create_tables(conn_str)
    create_functions(conn_str)
    insert_static_data(conn_str)


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
    create_all(c_str)
