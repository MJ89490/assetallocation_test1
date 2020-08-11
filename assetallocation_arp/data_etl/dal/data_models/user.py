from typing import Optional


# noinspection PyAttributeOutsideInit
class User:
    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name = name
        self._email = None

    @property
    def user_id(self) -> str:
        return self._user_id

    @user_id.setter
    def user_id(self, x: str) -> None:
        self._user_id = x

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, x: str) -> None:
        self._name = x

    @property
    def email(self) -> Optional[str]:
        return self._email

    @email.setter
    def email(self, x: str):
        self._email = x
