class UserAccountModel:
    def __init__(self, first_name, last_name, password):
        self.validate_name(first_name, last_name)
        self.validate_password(password)

        self.first_name = first_name
        self.last_name = last_name
        self.password = hash(password)

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
