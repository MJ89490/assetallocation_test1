class User:
    def __init__(self, email: str, user_id: str, name: str):
        self._email = email
        self._user_id = user_id
        self._name = name

    @property
    def user_id(self):
        return self._user_id
