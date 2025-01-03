from typing import Any

from asgiref.sync import sync_to_async
from django.db import models

from src.core.db.fields import PrecisedFloatField
from src.core.exception import ValidationError, NotFoundError


class AsyncQuerySet(models.Manager):
    """
    Async manager to handle async operations.
    """

    async def aget(self, *args, **kwargs):
        try:
            return await super().aget(*args, **kwargs)
        except self.model.DoesNotExist:
            raise NotFoundError(f"{self.model.__name__} not found.")

    async def aselect_related(self, *fields):
        return await sync_to_async(self.select_related)(*fields)


class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    objects = AsyncQuerySet()

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.__class__.__name__}_{self.pk}"

    def set_prefetch(self, name: str, value: Any) -> None:
        """
        Special method to set child object to the cache, to avoid extra queries and async problems in ninja.
        """
        self._prefetched_objects_cache = {name: value}


class BaseMacroModel(BaseModel):
    fat = PrecisedFloatField()
    protein = PrecisedFloatField()
    carb = PrecisedFloatField()
    kcal = PrecisedFloatField()

    class Meta:
        abstract = True

    def clean(self):
        if all(not getattr(self, field) for field in ["fat", "protein", "carb"]):
            raise ValidationError(
                f"At least one macro must be provided or have a value greater than 0."
            )
        if not self.kcal:
            raise ValidationError("Kcal must be provided.")
