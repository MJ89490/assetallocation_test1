from pathlib import Path
from glob import iglob
from typing import List, Iterator


def get_function_sql_files() -> Iterator[List[str]]:
    """Return ordered iterator of sql files required to build triggers"""
    return reversed([f for f in iglob(str(Path(__file__).parent / '**/*.sql'), recursive=True)])
