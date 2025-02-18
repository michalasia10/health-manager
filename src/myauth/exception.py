from src.core.exception import ValidationError


class TokenExpire(ValidationError):
    def __init__(self, message: str = "Token expired.") -> None:
        super().__init__(message)


class TokenInvalid(ValidationError):
    def __init__(self, message: str = "Token invalid.") -> None:
        super().__init__(message)
