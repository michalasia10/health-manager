from dataclasses import dataclass

from typing import Optional, ClassVar

from src.core.validator.base import Validator


@dataclass
class Entity:
    VALIDATORS: ClassVar[list[Optional[type[Validator]]]] = []

    def validate(self, *args, **kwargs):
        assert all(issubclass(validator, Validator) for validator in self.VALIDATORS), (
            f"VALIDATORS must be a list of {Validator.__name__} instances."
        )
        for validator in self.VALIDATORS:
            validator(self).validate(*args, **kwargs)

        return self
