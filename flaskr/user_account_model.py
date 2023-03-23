import hashlib


class UserAccountModel:
    """Represents a user account for creating an account, or logging in."""
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
        """Throws an exception if the first or last name fields are left blank."""
        if not first_name:
            raise TypeError("Please enter your first name")
        if not last_name:
            raise TypeError("Please enter your last name")

    @staticmethod
    def validate_password(password):
        """Throws an exception if the password field is left blank."""
        if not password:
            raise TypeError("Please enter your password")

    @staticmethod
    def validate_role(role):
        """Throws an exception if the role is an invalid number.
        Role can be blank so that the model can be used to log in as well as create an account."""
        if role is not None:
            if 4 <= int(role) <= 0:
                raise TypeError("Invalid role")

    @staticmethod
    def hash_password(password):
        """Hash a given password using Python's hashlib module. The hash is returned as a string of characters."""
        salt = "0"
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 5).hex()

