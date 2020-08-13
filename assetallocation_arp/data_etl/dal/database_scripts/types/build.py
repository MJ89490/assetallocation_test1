from pathlib import Path
from glob import iglob


def get_type_sql_files():
    return [f for f in iglob(str(Path(__file__).parent / '**/*.sql'), recursive=True)]
