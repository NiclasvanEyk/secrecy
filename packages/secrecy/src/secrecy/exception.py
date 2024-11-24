"""
Base exception classes and other core exception handling utilities.
"""

class SecrecyError(BaseException):
    """The base class for all errors thrown by secrecy."""


class MissingEnvironmentVariableError(SecrecyError):
    def __init__(self, environment_variable_name: str, secret_name: str) -> None:
        self.environment_variable_name = environment_variable_name
        self.secret_name = secret_name
        message = f"The {secret_name} secret requires the {self.environment_variable_name} environment variable, but it seems to be empty"
        super().__init__(message)
