from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context


class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.password_hash = ""

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)



