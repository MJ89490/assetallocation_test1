class User:
    def __init__(self, user_id: str, name: str):
        self._user_id = user_id
        self._name = name
        self._email = None

    @property
    def user_id(self):
        return self._user_id

    @property
    def email(self):
        return self._email

    # TODO should there be validation here for lgim.com emails only?
    @email.setter
    def email(self, x: str):
        self._email = x
