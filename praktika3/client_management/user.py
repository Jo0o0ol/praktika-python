class User:
    def __init__(self, username, password, is_admin):
        self.username = username
        self.password = password
        self.is_admin = is_admin

    def login(self, username, password):
        return self.username == username and self.password == password
