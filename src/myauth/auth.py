from typing import Optional, Any

from django.http import HttpRequest
from ninja.security import APIKeyHeader


class AuthorizationHeader(APIKeyHeader):
    param_name = "Authorization"

    def authenticate(self, request: HttpRequest, key: Optional[str]) -> Optional[Any]:
        pass


class RefreshHeader(APIKeyHeader):
    param_name = "Refresh"

    def authenticate(self, request: HttpRequest, key: Optional[str]) -> Optional[Any]:
        pass


# Note:  whole authentication is by dedicated service which is used by middleware.
#       this list is only as helper for `openapi` to display `Authentication` button
auth_list: list[APIKeyHeader] = [
    AuthorizationHeader(),
    RefreshHeader(),
]
