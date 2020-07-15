from psycopg2.extras import DateTimeTZRange

from .user import User


class Strategy:
    def __init__(self, description: str, strategy_id: int, name: str, system_tstzrange: DateTimeTZRange, user: User):
        self._description = description
        self._strategy_id = strategy_id
        self._name = name
        self._system_tstzrange = system_tstzrange
        self._user_id = user
