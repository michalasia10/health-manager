import inspect
from functools import partial, wraps
from typing import Any, Union, List, AsyncGenerator, Callable, Type

from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.module_loading import import_string
from ninja.conf import settings
from ninja.constants import NOT_SET
from ninja.errors import ConfigError
from ninja.pagination import (
    make_response_paginated,
    PaginationBase,
    AsyncPaginationBase,
)
from ninja.utils import (
    contribute_operation_args,
    contribute_operation_callback,
    is_async_callable,
)


def paginate(func_or_pgn_class: Any = NOT_SET, **paginator_params: Any) -> Callable:
    """
    Custom pagination till `paginate` will be fixed in ninja.
    """

    isfunction = inspect.isfunction(func_or_pgn_class)
    isnotset = func_or_pgn_class == NOT_SET

    pagination_class: Type[Union[PaginationBase, AsyncPaginationBase]] = import_string(
        settings.PAGINATION_CLASS
    )

    if isfunction:
        return _inject_pagination(func_or_pgn_class, pagination_class)

    if not isnotset:
        pagination_class = func_or_pgn_class

    def wrapper(func: Callable) -> Any:
        return _inject_pagination(func, pagination_class, **paginator_params)

    return wrapper


def _inject_pagination(
    func: Callable,
    paginator_class: Type[Union[PaginationBase, AsyncPaginationBase]],
    **paginator_params: Any,
) -> Callable:
    paginator = paginator_class(**paginator_params)
    if is_async_callable(func):
        if not hasattr(paginator, "apaginate_queryset"):
            raise ConfigError("Pagination class not configured for async requests")

        @wraps(func)
        async def view_with_pagination(request: HttpRequest, **kwargs: Any) -> Any:
            pagination_params = kwargs.pop("ninja_pagination")
            if paginator.pass_parameter:
                kwargs[paginator.pass_parameter] = pagination_params

            items = await func(request, **kwargs)

            result = await paginator.apaginate_queryset(
                items, pagination=pagination_params, request=request, **kwargs
            )

            async def evaluate(results: Union[List, QuerySet]) -> AsyncGenerator:
                async for result in results:
                    yield result

            if paginator.Output:  # type: ignore
                result[paginator.items_attribute] = [
                    result
                    async for result in evaluate(result[paginator.items_attribute])
                ]
            return result

    else:

        @wraps(func)
        def view_with_pagination(request: HttpRequest, **kwargs: Any) -> Any:
            pagination_params = kwargs.pop("ninja_pagination")
            if paginator.pass_parameter:
                kwargs[paginator.pass_parameter] = pagination_params

            items = func(request, **kwargs)

            result = paginator.paginate_queryset(
                items, pagination=pagination_params, request=request, **kwargs
            )
            if paginator.Output:  # type: ignore
                result[paginator.items_attribute] = list(
                    result[paginator.items_attribute]
                )
                # ^ forcing queryset evaluation #TODO: check why pydantic did not do it here
            return result

    contribute_operation_args(
        view_with_pagination,
        "ninja_pagination",
        paginator.Input,
        paginator.InputSource,
    )

    if paginator.Output:  # type: ignore
        contribute_operation_callback(
            view_with_pagination,
            partial(make_response_paginated, paginator),
        )

    return view_with_pagination
