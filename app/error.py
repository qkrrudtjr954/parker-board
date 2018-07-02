
class NotFoundError(Exception):
    def __init__(self, message):
        self.message = message


class AuthenticationError(Exception):
    pass


class DuplicateValueError(Exception):
    def __init__(self, message):
        self.message = message


class SameDataError(Exception):
    def __init__(self, message):
        self.message = message


class WrongPasswordError(Exception):
    def __init__(self, message):
        self.message = message

