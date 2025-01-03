import logfire


class CoreException(Exception):
    def __init__(self, message: str, status_code: int) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        logfire.info(
            "[{class_name}-{status_code}] | {message}",
            class_name=self.__class__.__name__,
            message=self.message,
            status_code=self.status_code,
        )

    def __str__(self):
        return f"{self.status_code} | self.message"

    __repr__ = __str__


class ValidationError(CoreException):
    def __init__(self, message: str, status_code: int = 400) -> None:
        super().__init__(message, status_code)
