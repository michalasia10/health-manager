from dataclasses import dataclass
from enum import Enum
from typing import Optional, ClassVar

from src.core.entity import Entity
from src.myauth.validator.auth import AuthMandatoryValuesValidator


class EnumAuthType(str, Enum):
    EMAIL = "email"
    GOOGLE = "google"


@dataclass
class AuthEntity(Entity):
    VALIDATORS: ClassVar = [
        AuthMandatoryValuesValidator,
    ]

    type: EnumAuthType

    redirect_url: Optional[str] = None

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
