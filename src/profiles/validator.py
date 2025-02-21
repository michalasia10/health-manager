from src.core.exception import DomainError
from src.core.validator.base import Validator
from src.profiles.models import UserProfile


class ProfileValidator(Validator):
    def validate(self, manual=False) -> None:
        self.model_instance: UserProfile

        if manual and self.model_instance.role == self.model_instance.Roles.DIETETIC:
            raise DomainError("User can't granted to dietetic by himself")
