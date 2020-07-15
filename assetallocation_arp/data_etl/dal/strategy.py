from typing import Optional

from .user import User


class Strategy:
    def __init__(self, name: str, user: User, description: Optional[str] = None):
        self._description = description
        self._strategy_id = None
        self._name = name
        self._system_tstzrange = None
        self._user = user

    @property
    def user(self):
        return self._user

    @property
    def description(self):
        return self._description

    @property
    def system_tstzrange(self):
        return self._system_tstzrange

    @property
    def name(self):
        return self._name

    def insert(self, *args):
        """insert strategy into database"""
        pass

