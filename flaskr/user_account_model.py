import os
import hashlib

os.environ["PYTHONHASHSEED"] = "0"


class UserAccountModel:
    def __init__(self, first_name, last_name, password, role):
        self.validate_name(first_name, last_name)
        self.validate_password(password)

        self.first_name = first_name
        self.last_name = last_name
        self.password = self.hash_password(password)
        self.role = role

    @staticmethod
    def validate_name(first_name, last_name):
        if not first_name:
            raise Exception("Please enter your first name")
        if not last_name:
            raise Exception("Please enter your last name")

    @staticmethod
    def validate_password(password):
        if not password:
            raise Exception("Please enter your password")

    @staticmethod
    def hash_password(password):
        salt = "0"
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 5).hex()
