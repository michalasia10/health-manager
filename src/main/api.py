from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from ninja import NinjaAPI

from src.core.exception import CoreException
from src.plans.api import router

api = NinjaAPI(title="health-manager")

api.add_router("/plans/", router)


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
    request, exc: ObjectDoesNotExist
) -> HttpResponse:
    return api.create_response(
        request,
        dict(
            detail="Object not found.",
            status=404,
        ),
        status=404,
    )
