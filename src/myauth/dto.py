from typing import Optional

from ninja import Schema
from pydantic import EmailStr
from src.myauth.entity.auth import EnumAuthType


class AuthSignupInputDto(Schema):
    type: EnumAuthType

    redirect_url: Optional[str] = None

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class AuthLoginInputDto(Schema):
    redirect_url: Optional[str] = None

    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserDto(Schema):
    id: str
    role: str
    is_anonymous: bool


class SessionDto(Schema):
    access_token: str
    refresh_token: str


class AuthOutputDto(Schema):
    user: UserDto
    session: Optional[SessionDto]
