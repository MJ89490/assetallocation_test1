from pathlib import Path
from glob import iglob
from typing import List


def get_trigger_sql_files() -> List[str]:
    """Return list of sql files required to build triggers"""
    return [f for f in iglob(str(Path(__file__).parent / '**/*.sql'), recursive=True)]
