import typing

from src.core.exception import DomainError
from src.core.validator.base import Validator

if typing.TYPE_CHECKING:
    from src.myauth.entity import AuthEntity


class AuthMandatoryValuesValidator(Validator):
    def validate(self) -> None:
        from src.myauth.entity.auth import EnumAuthType

        self.model_instance: "AuthEntity"
        _type = self.model_instance.type

        match _type:
            case EnumAuthType.EMAIL:
                if not all([self.model_instance.email, self.model_instance.password]):
                    raise DomainError(
                        "Email and password are required for email type auth."
                    )
            case EnumAuthType.GOOGLE:
                if not self.model_instance.redirect_url:
                    raise DomainError("Redirect url is required for google type auth.")
