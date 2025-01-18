from abc import ABC, abstractmethod
from typing import TypeVar

from django.db.models import Model

MInstance = TypeVar("MInstance", bound=Model)


class Validator(ABC):
    def __init__(self, model_instance: MInstance) -> None:
        self.model_instance = model_instance

    @abstractmethod
    def validate(self, *args, **kwargs) -> None:
        pass
