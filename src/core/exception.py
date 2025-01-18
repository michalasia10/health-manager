from typing import Optional, Any

from src.core.log import log


class CoreException(Exception):
    def __init__(
        self, message: str, status_code: int, extra: Optional[dict[str, Any]] = None
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        log(
            "[{class_name}-{status_code}] | {message}",
            extra=extra,
            class_name=self.__class__.__name__,
            message=self.message,
            status_code=self.status_code,
        )

    def __str__(self):
        return f"{self.status_code} | self.message"

    __repr__ = __str__


class ValidationError(CoreException):
    def __init__(
        self,
        message: str,
        status_code: int = 400,
        extra: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, status_code, extra=extra)


class DomainError(ValidationError):
    pass


class NotFoundError(CoreException):
    def __init__(
        self,
        message: str,
        status_code: int = 404,
        extra: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, status_code, extra)
