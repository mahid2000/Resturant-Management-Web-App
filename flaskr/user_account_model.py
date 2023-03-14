import hashlib


class UserAccountModel:
    def __init__(self, first_name, last_name, password, role):
        self.validate_name(first_name, last_name)
        self.validate_password(password)
        self.validate_role(role)

        self.first_name = first_name
        self.last_name = last_name
        self.password = self.hash_password(password)
        self.role = role

    @staticmethod
    def validate_name(first_name, last_name):
        if not first_name:
            raise TypeError("Please enter your first name")
        if not last_name:
            raise TypeError("Please enter your last name")

    @staticmethod
    def validate_password(password):
        if not password:
            raise TypeError("Please enter your password")

    @staticmethod
    def validate_role(role):
        if role is not None:
            if 4 <= int(role) <= 0:
                raise TypeError("Invalid role")

    @staticmethod
    def hash_password(password):
        salt = "0"
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 5).hex()

