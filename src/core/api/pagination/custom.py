from typing import Any, List

from django.db.models import QuerySet
from math import inf
from ninja import Schema
from ninja.conf import settings
from ninja.pagination import LimitOffsetPagination
from pydantic import Field

from src.core.api.pagination.ninja_fix import paginate


class CustomLimitOffsetPagination(LimitOffsetPagination):
    class Input(Schema):
        limit: int = Field(
            settings.PAGINATION_PER_PAGE,
            ge=1,
            le=settings.PAGINATION_MAX_LIMIT
            if settings.PAGINATION_MAX_LIMIT != inf
            else None,
        )
        offset: int = Field(0, ge=0)

    class Output(Schema):
        items: List[Any]
        count: int
        offset: int
        limit: int

    def paginate_queryset(
            self,
            queryset: QuerySet,
            pagination: Input,
            **params: Any,
    ) -> Any:
        offset = pagination.offset
        limit: int = min(pagination.limit, settings.PAGINATION_MAX_LIMIT)
        return {
            "count": self._items_count(queryset),
            "offset": offset,
            "limit": limit,
            "items": queryset[offset: offset + limit],
        }  # noqa: E203

    async def apaginate_queryset(
            self,
            queryset: QuerySet,
            pagination: Input,
            **params: Any,
    ) -> Any:
        offset = pagination.offset
        limit: int = min(pagination.limit, settings.PAGINATION_MAX_LIMIT)
        return {
            "count": await self._aitems_count(queryset),
            "offset": offset,
            "limit": limit,
            "items": queryset[offset: offset + limit],
        }  # noqa: E203


default_paginate = paginate(CustomLimitOffsetPagination)
