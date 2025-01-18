from src.core.log import log
from src.core.exception import DomainError
from src.core.validator.base import Validator


class DateTimeRangeValidator(Validator):
    def validate(self, *args, **kwargs) -> None:
        if (
            self.model_instance.end_date
            and self.model_instance.start_date > self.model_instance.end_date
        ):
            log(
                f"Start date: {self.model_instance.start_date} | End date: {self.model_instance.end_date}"
            )
            raise DomainError("End date must be greater than start date.")
