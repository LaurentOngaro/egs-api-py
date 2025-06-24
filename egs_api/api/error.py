"""
Error types for Epic API
"""


class EpicAPIError(Exception):
    """Base error for Epic API operations"""
    pass


class InvalidCredentialsError(EpicAPIError):
    """Invalid credentials provided"""
    pass


class APIError(EpicAPIError):
    """API error with specific message"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(f"API Error: {message}")


class UnknownError(EpicAPIError):
    """Unknown error occurred"""
    pass


class InvalidParamsError(EpicAPIError):
    """Invalid parameters provided"""
    pass


class ServerError(EpicAPIError):
    """Server error occurred"""
    pass


class FabTimeoutError(EpicAPIError):
    """Fab timeout error"""
    pass
