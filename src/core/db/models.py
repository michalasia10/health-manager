from typing import Any

from asgiref.sync import sync_to_async
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.db import models

from src.core.db.fields import PrecisedFloatField
from src.core.entity import Entity
from src.core.exception import NotFoundError
from src.core.validator.macro import MacroValidator


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


class BaseModel(models.Model, Entity):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    objects = AsyncQuerySet()

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.__class__.__name__}_{self.pk}"

    def full_clean(
        self,
        exclude=None,
        validate_unique=True,
        validate_constraints=True,
        *args,
        **kwargs,
    ):
        """
        Override of the full_clean method pass extra arguments to the validate method.
        """
        errors = {}
        if exclude is None:
            exclude = set()
        else:
            exclude = set(exclude)

        try:
            self.clean_fields(exclude=exclude)
        except ValidationError as e:
            errors = e.update_error_dict(errors)

        # Form.clean() is run even if other validation fails, so do the
        # same with Model.clean() for consistency.
        try:
            self.clean(*args, **kwargs)
        except ValidationError as e:
            errors = e.update_error_dict(errors)

        # Run unique checks, but only for fields that passed validation.
        if validate_unique:
            for name in errors:
                if name != NON_FIELD_ERRORS and name not in exclude:
                    exclude.add(name)
            try:
                self.validate_unique(exclude=exclude)
            except ValidationError as e:
                errors = e.update_error_dict(errors)

        # Run constraints checks, but only for fields that passed validation.
        if validate_constraints:
            for name in errors:
                if name != NON_FIELD_ERRORS and name not in exclude:
                    exclude.add(name)
            try:
                self.validate_constraints(exclude=exclude)
            except ValidationError as e:
                errors = e.update_error_dict(errors)

        if errors:
            raise ValidationError(errors)

    def clean(self, *args, **kwargs):
        super().clean()
        self.validate(*args, **kwargs)

    def set_prefetch(self, name: str, value: Any) -> None:
        """
        Special method to set child object to the cache, to avoid extra queries and async problems in ninja.
        """
        self._prefetched_objects_cache = {name: value}


class BaseMacroModel(BaseModel):
    VALIDATORS = [
        MacroValidator,
    ]

    fat = PrecisedFloatField()
    protein = PrecisedFloatField()
    carb = PrecisedFloatField()
    kcal = PrecisedFloatField()

    class Meta:
        abstract = True
