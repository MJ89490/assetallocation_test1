from pathlib import Path
from glob import iglob
from typing import List


def get_type_sql_files() -> List[str]:
    """Return list of sql files required to build types"""
    parent_types = ['frequency.sql']
    types = [f for f in iglob(str(Path(__file__).parent / '**/*.sql'), recursive=True)]
    return sorted(types, key=lambda x: any(x.endswith(f'\\{i}') for i in parent_types), reverse=True)
