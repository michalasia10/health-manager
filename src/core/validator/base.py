import typing
from abc import ABC, abstractmethod


class Validator(ABC):
    def __init__(self, model_instance: typing.Any) -> None:
        self.model_instance = model_instance

    @abstractmethod
    def validate(self, *args, **kwargs) -> None:
        pass
