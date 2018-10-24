from werkzeug.security import generate_password_hash

users = []

cool_user_sample = {
    'name': 'Evil Cow',
    'username': 'e-cow',
    'email': 'ecow@isus.mammals',
    'password': generate_password_hash('wah!-things-we-do!'),
    'user id': 1
}


class Users(object):
    """docstring for Users"""
    def __init__(self, name, username, email, password):
        super(Users, self).__init__()
        self.name = name
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def usersList():
        users.append(cool_user_sample)

        return users
