from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context


class User(UserMixin):
    def __init__(self, id):
        self.id = id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True





