from passlib.hash import pbkdf2_sha256 as hash_pass


class Users():
    def __init__(self, name, username, email, password):
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.id = 0

    @staticmethod
    def hashpasses(password):
        return hash_pass.hash(password)


class RevokeToken:
    pass
