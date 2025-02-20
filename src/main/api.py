from http import HTTPStatus

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from gotrue.errors import AuthError
from ninja import NinjaAPI

from src.core.exception import CoreException
from src.myauth.api import router as myauth_router
from src.myauth.auth import auth_list
from src.plans.api import router as plans_router

api = NinjaAPI(
    title="health-manager",
    auth=auth_list,
    csrf=True,
)

api.add_router("/plans/", plans_router)
api.add_router("/auth/", myauth_router)


@api.exception_handler(CoreException)
def django_validation_exception(request, exc: CoreException) -> HttpResponse:
    return api.create_response(
        request,
        dict(
            detail=exc.message,
            status=exc.status_code,
        ),
        status=exc.status_code,
    )


@api.exception_handler(ObjectDoesNotExist)
def django_object_does_not_exist_exception(
    request,
    exc: ObjectDoesNotExist,
) -> HttpResponse:
    return api.create_response(
        request,
        dict(
            detail="Object not found.",
            status=HTTPStatus.NOT_FOUND,
        ),
        status=HTTPStatus.NOT_FOUND,
    )


@api.exception_handler(AuthError)
def supabase_auth_error(
    request,
    exc: AuthError,
) -> HttpResponse:
    code = (
        HTTPStatus.BAD_REQUEST
        if exc.code
        in [
            "validation_failed",
            "email_exists",
            "phone_exists",
            "weak_password",
            "user_already_exists",
        ]
        else HTTPStatus.UNAUTHORIZED
    )

    return api.create_response(
        request,
        dict(
            detail=exc.message,
            status=code,
            supabase_code=exc.code,
        ),
        status=code,
    )
