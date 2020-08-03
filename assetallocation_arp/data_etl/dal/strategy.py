from typing import Optional
from abc import ABC


class Strategy(ABC):
    def __init__(self, name: str, description: Optional[str] = None):
        self._description = description
        self._name = name
        self._version = None

    @property
    def description(self):
        return self._description

    @property
    def system_tstzrange(self):
        return self._version

    @property
    def name(self):
        return self._name
