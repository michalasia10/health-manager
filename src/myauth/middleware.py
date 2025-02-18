from asyncio import iscoroutinefunction
from urllib.request import Request

from asgiref.sync import markcoroutinefunction

from src.myauth.service import AuthService

auth_service = AuthService()

URLS_TO_EXCLUDE = [
    "/signup",
    "/login",
    "docs",
    "openapi",
]


class AsyncUserMiddleware:
    async_capable = True
    sync_capable = False

    def __init__(self, get_response):
        self.get_response = get_response
        if iscoroutinefunction(self.get_response):
            markcoroutinefunction(self)

    async def __call__(self, request: Request):
        if any(url in request.path for url in URLS_TO_EXCLUDE):
            return await self.get_response(request)

        request.user = await auth_service.get_user_from_token(
            access_token=request.headers.get("Authorization"),
            refresh_token=request.headers.get("Refresh"),
        )

        return await self.get_response(request)
