from datetime import datetime

class Users:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.joined = datetime.now()

    