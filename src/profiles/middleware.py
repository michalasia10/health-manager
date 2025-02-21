from asyncio import iscoroutinefunction

from asgiref.sync import markcoroutinefunction

from src.core.types import RequestT
from src.myauth.service import AuthService
from src.profiles.service import get_or_create_profile

auth_service = AuthService()


class AsyncUserProfileMiddleware:
    async_capable = True
    sync_capable = False

    def __init__(self, get_response):
        self.get_response = get_response
        if iscoroutinefunction(self.get_response):
            markcoroutinefunction(self)

    async def __call__(self, request: RequestT):
        request.profile = await get_or_create_profile(user_id=request.user.id)

        return await self.get_response(request)
