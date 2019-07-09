"""
Regroup all exceptions concerning the Models
and the communication with the Database.
"""


class ModelCreationError(Exception):
    """
    Error during a model creation
    """

    def __init__(self, error_code, params=None):
        self.error_code = error_code
        self.params = params


class EntityNotFound(Exception):
    """
    Missing entity in database
    """

    def __init__(self, error_code, params=None):
        self.error_code = error_code
        self.params = params


class ModelUpdateError(Exception):
    """
    Error during a model update
    """

    def __init__(self, error_code, params=None):
        self.error_code = error_code
        self.params = params


class DatabaseError(Exception):
    """
    Unknown database error
    """

    def __init__(
            self,
            message
    ):
        self.message = message  # pragma: no cover
