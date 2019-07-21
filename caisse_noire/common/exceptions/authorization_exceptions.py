"""
Regroup all exceptions concerning the user identity.
"""


class AuthorizationError(Exception):
    """
    Error during user authorization
    """

    def __init__(self, error_code, params=None):
        self.error_code = error_code
        self.params = params
