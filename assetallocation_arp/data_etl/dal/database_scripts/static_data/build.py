from pathlib import Path
from glob import iglob


def get_static_data_sql_files():
    return [f for f in iglob(str(Path(__file__).parent / '**/*.sql'), recursive=True)]
