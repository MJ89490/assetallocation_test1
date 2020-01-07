from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
"""
Class to connect to the database
return: JSON ???
"""
#connection with the Login Form
class ConnectionDatabase(UserMixin):
    def __init__(self):
        self.password_origin = "abcd" #take from the database???

    def set_password(self):
        """
            password: password of the user
            The function create a password hashing, similar to a long encoded key
        """
        self.password_hash = generate_password_hash(self.password_origin)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "Password {}".format(self.password_hash)


"""
Class to collect the data depending on the model the user asked for
return: ???
"""

class CollectData(ConnectionDatabase):

    def __init__(self):
        pass
    def data_db(self):
        pass