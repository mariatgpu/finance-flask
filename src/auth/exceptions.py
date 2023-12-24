from src.common.exceptions import BadRequest


class IncorrectUsername(BadRequest):
    def __init__(
        self,
        message="Username must be at least 4 characters long and contain only latin upper and lower case characters, digits and ._",
    ):
        BadRequest.__init__(self, message)


class IncorrectPassword(BadRequest):
    def __init__(
        self,
        message="Password must be at least 8 characters long and contain uppercase and lowercase characters, digits and special symbols (@$()!%*?&)",
    ):
        BadRequest.__init__(self, message)


class IncorrectUsernameOrPassword(BadRequest):
    def __init__(self):
        BadRequest.__init__(self, "Incorrect username or password")
