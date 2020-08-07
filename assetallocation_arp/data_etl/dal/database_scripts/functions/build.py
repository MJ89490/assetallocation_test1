from pathlib import Path
from glob import iglob

from assetallocation_arp.data_etl.dal.database_scripts.build import execute_script_files


def create_functions(conn_str):
    files = [f for f in iglob(str(Path(__file__).parent / '**/*.sql'), recursive=True)]
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
    create_functions(c_str)
