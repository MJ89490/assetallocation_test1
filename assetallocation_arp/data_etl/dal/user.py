from typing import Optional


class User:
    def __init__(self, user_id: str, email: Optional[str]= None, name: Optional[str] = None):
        self._email = email
        self._user_id = user_id
        self._name = name

    @property
    def user_id(self):
        return self._user_id
