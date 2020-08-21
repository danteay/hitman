"""
Common project errors
"""


class HandlerError(Exception):
    """
    Generic handler error
    :param code: HTTP status code
    :param message: Error message
    :param errors: additional errors
    """

    def __init__(self, code, message, errors=None):
        super().__init__(message, errors)
        self.message = message
        self.code = code

    def get_message(self):
        """Get error message"""
        return self.message

    def get_code(self):
        """Get error code"""
        return self.code


class UserConflict(HandlerError):
    """
    Custom error for user registration conflict
    :param errors: Additional errors
    """

    def __init__(self, errors=None):
        super().__init__(409, "user-conflict", errors)


class UnauthorizedUser(HandlerError):
    """
    Custom error for not found users
    :param errors: Additional errors
    """

    def __init__(self, errors=None):
        super().__init__(401, "unauthorized", errors)
