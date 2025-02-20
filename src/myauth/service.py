from http import HTTPStatus
from typing import Literal


from src.core.exception import ValidationError
from src.myauth.clients.supabase import SupabaseAuthClient
from src.myauth.dto import AuthSignupInputDto, AuthLoginInputDto, AuthOutputDto
from src.myauth.entity.auth import AuthEntity, EnumAuthType
from src.myauth.entity.token import TokenEntity
from src.myauth.exception import TokenExpire, TokenInvalid


class AuthService:
    def __init__(self, client_type: Literal["supabase"] = "supabase") -> None:
        self.client_type = client_type

    @property
    def client(self):
        match self.client_type:
            case "supabase":
                return SupabaseAuthClient()
            case _:
                raise ValueError("Invalid client type")

    async def get_user_from_token(
        self,
        access_token: str | None,
        refresh_token: str | None,
    ) -> AuthOutputDto:
        token = TokenEntity(
            access_token=access_token,
            refresh_token=refresh_token,
        )

        if token.empty_token:
            result = await self.client.sign_in_sign_in_anonymously()
            return AuthOutputDto(**result)

        try:
            token.validate()
        except TokenInvalid as e:
            raise e
        except TokenExpire:
            result = await self.client.refresh_token(token.refresh_token)
        else:
            result = await self.client.retrieve_user(token.access_token)

        return AuthOutputDto(**result)

    async def sign_up(self, dto: AuthSignupInputDto) -> AuthOutputDto:
        entity = AuthEntity(**dto.dict())
        entity.validate()

        match entity.type:
            case EnumAuthType.EMAIL:
                result = await self.client.email_sign_up(
                    email=entity.email,
                    password=entity.password,
                    first_name=entity.first_name,
                    last_name=entity.last_name,
                )
            case _:
                raise ValidationError(
                    message=f"Not supported auth type: {entity.type}",
                    status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                )
        return AuthOutputDto(**result)

    async def login(self, dto: AuthLoginInputDto) -> AuthOutputDto:
        entity = AuthEntity(**dto.dict())
        entity.validate()

        match entity.type:
            case EnumAuthType.EMAIL:
                result = await self.client.email_login(
                    email=entity.email,
                    password=entity.password,
                )
            case _:
                raise ValidationError(
                    message=f"Not supported auth type: {entity.type}",
                    status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                )
        return AuthOutputDto(**result)
