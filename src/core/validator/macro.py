from src.core.exception import DomainError
from src.core.log import log
from src.core.validator.base import Validator


class MacroValidator(Validator):
    def validate(self, *args, **kwargs) -> None:
        values = [
            getattr(self.model_instance, field) for field in ["fat", "protein", "carb"]
        ]
        if all(not value for value in values):
            log("Values: {values}", values=values)
            raise DomainError(
                "At least one macro must be provided or have a value greater than 0."
            )
        if not self.model_instance.kcal:
            raise DomainError("Kcal must be provided.")
