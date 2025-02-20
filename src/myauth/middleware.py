from asyncio import iscoroutinefunction
from urllib.request import Request

from asgiref.sync import markcoroutinefunction
from django.http import JsonResponse

from src.core.exception import CoreException
from src.myauth.entity.user import UserEntity
from src.myauth.service import AuthService

auth_service = AuthService()


class AsyncUserMiddleware:
    async_capable = True
    sync_capable = False

    def __init__(self, get_response):
        self.get_response = get_response
        if iscoroutinefunction(self.get_response):
            markcoroutinefunction(self)

    async def __call__(self, request: Request):
        try:
            auth = await auth_service.get_user_from_token(
                access_token=request.headers.get("Authorization"),
                refresh_token=request.headers.get("Refresh"),
            )
        except CoreException as e:
            return JsonResponse(
                dict(
                    detail=e.message,
                    status=e.status_code,
                ),
                status=e.status_code,
            )

        request.user = UserEntity(
            id=auth.user.id,
            role=auth.user.role,
            is_anonymous=auth.user.is_anonymous,
        )

        return await self.get_response(request)
