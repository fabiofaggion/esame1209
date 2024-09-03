from flask_login import UserMixin

class User(UserMixin):
   def __init__(self, id, username, password, user_type):
        self.id = id
        self.username = username
        self.password = password
        self.user_type = user_type