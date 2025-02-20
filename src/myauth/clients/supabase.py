from asyncio import sleep
from typing import Any

from django.conf import settings
from gotrue import Session, User
from gotrue.errors import AuthRetryableError
from supabase._async.client import AsyncClient as Client
from supabase._async.client import create_client
from datetime import datetime
from src.myauth.clients.base import AuthClient
import uuid


async def signup_with_retry(supabase, email, password, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await supabase.auth.sign_up({"email": email, "password": password})
        except AuthRetryableError:
            if attempt == max_retries - 1:
                raise

            await sleep(1 * (attempt + 1))


class SupabaseAuthClient(AuthClient):
    @staticmethod
    async def get_client() -> Client:
        return await create_client(
            supabase_url=settings.SUPABASE_URL,
            supabase_key=settings.SUPABASE_KEY,
        )

    async def retrieve_user(self, access_token: str) -> dict[str, Any]:
        client = await self.get_client()

        response = await client.auth.get_user(jwt=access_token)
        user: User = response.user

        return dict(
            user=dict(
                id=user.id,
                role=user.role,
                is_anonymous=user.is_anonymous,
            ),
            session=None,
        )

    async def sign_in_sign_in_anonymously(self) -> dict[str, Any]:
        client = await self.get_client()

        response = await client.auth.sign_in_anonymously(
            credentials=dict(
                data=dict(
                    email=f"anononymus_{datetime.now()}@gmail.com",
                    password=uuid.uuid4(),
                    options=dict(
                        data=dict(
                            first_name=f"ANON_{datetime.now()}",
                            last_name=f"ANON_{datetime.now()}",
                            org_role="",
                        ),
                    ),
                ),
                captcha_token="",
            )
        )

        session: Session = response.session
        user: User = response.user

        return dict(
            user=dict(
                id=user.id,
                role=user.role,
                is_anonymous=user.is_anonymous,
            ),
            session=dict(
                access_token=session.access_token,
                refresh_token=session.refresh_token,
            ),
        )

    async def refresh_token(self, refresh_token: str) -> dict[str, Any]:
        client = await self.get_client()

        response = await client.auth.refresh_session(
            refresh_token=refresh_token,
        )
        session: Session = response.session
        user: User = response.user

        return dict(
            user=dict(
                id=user.id,
                role=user.role,
                is_anonymous=user.is_anonymous,
            ),
            session=dict(
                access_token=session.access_token,
                refresh_token=session.refresh_token,
            ),
        )

    async def email_login(self, email: str, password: str) -> dict[str, Any]:
        client = await self.get_client()

        response = await client.auth.sign_in(
            dict(
                email=email,
                password=password,
            )
        )
        session: Session = response.session
        user: User = response.user

        return dict(
            user=dict(
                id=user.id,
                role=user.role,
                is_anonymous=user.is_anonymous,
            ),
            session=dict(
                access_token=session.access_token,
                refresh_token=session.refresh_token,
            ),
        )

    def google_sign_up(self, redirect_url: str) -> None:
        pass

    async def email_sign_up(
        self, email: str, password: str, first_name: str, last_name: str
    ) -> dict[str, Any]:
        client = await self.get_client()

        # try:
        response = await client.auth.sign_up(
            dict(
                email=email,
                password=password,
                options=dict(
                    data=dict(
                        first_name=first_name,
                        last_name=last_name,
                        org_role="",
                    ),
                ),
            )
        )

        session: Session = response.session
        user: User = response.user

        return dict(
            user=dict(
                id=user.id,
                role=user.role,
                is_anonymous=user.is_anonymous,
            ),
            session=dict(
                access_token=session.access_token,
                refresh_token=session.refresh_token,
            ),
        )
