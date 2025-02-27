class User:
    def __init__(self, username, password, is_admin=False):
        self.username = username
        self.password = password
        self.is_admin = is_admin

    def __str__(self):
        return f"{self.username} ({'Администратор' if self.is_admin else 'Пользователь'})"

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password, is_admin=True)
