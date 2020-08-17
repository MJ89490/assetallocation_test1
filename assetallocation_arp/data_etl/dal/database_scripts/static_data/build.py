from pathlib import Path
from glob import iglob
from typing import List


def get_static_data_sql_files() -> List[str]:
    """Return list of sql files required to add static data to database"""
    return [f for f in iglob(str(Path(__file__).parent / '**/*.sql'), recursive=True)]
