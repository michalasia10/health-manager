from dataclasses import dataclass
from typing import ClassVar, Optional

import jwt
from django.conf import settings

from src.core.entity import Entity
from src.myauth.validator.token import TokenValidator


@dataclass
class TokenEntity(Entity):
    VALIDATORS: ClassVar[list] = [
        TokenValidator,
    ]

    access_token: Optional[str]
    refresh_token: Optional[str]

    @property
    def empty_token(self):
        return self.access_token is None

    def get_decoded_access_token(self) -> dict:
        return jwt.decode(
            self.access_token,
            settings.SUPABASE_JWT_SECRET,
            algorithms=[settings.SUPABASE_ALGORITHM],
            audience=settings.SUPABASE_AUDIENCE,
            options=dict(
                verify_signature=True,
            ),
        )

    def get_user_id(self) -> str:
        return self.get_decoded_access_token().get("sub", "not-found")
