class ApplicationError(Exception):
    def __init__(self, message: str, code: int):
        self.message = message
        self.code = code


class BadRequest(ApplicationError):
    def __init__(self, message: str):
        ApplicationError.__init__(self, message, 400)


class Unauthorized(ApplicationError):
    def __init__(self, message: str):
        ApplicationError.__init__(self, message, 401)


class NotFound(ApplicationError):
    def __init__(self, message: str):
        ApplicationError.__init__(self, message, 404)


class InternalServerError(ApplicationError):
    def __init__(self):
        ApplicationError.__init__(self, "Something went wrong on the server", 500)


class UserNotFound(NotFound):
    def __init__(self):
        NotFound.__init__(self, "User with specified id not found")
