import time
import typing

import jwt

from src.core.validator.base import Validator
from src.myauth.exception import TokenExpire, TokenInvalid

if typing.TYPE_CHECKING:
    from src.myauth.entity.token import TokenEntity


class TokenValidator(Validator):
    def validate(self) -> None:
        self.model_instance: "TokenEntity"

        try:
            decoded = self.model_instance.get_decoded_access_token()
        except jwt.ExpiredSignatureError:
            raise TokenInvalid()
        except Exception:
            raise TokenInvalid()

        if decoded.get("exp", 0) < time.time():
            raise TokenExpire()
