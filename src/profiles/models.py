from django.db import models

from src.core.db.models import BaseModel
from src.core.entity import Entity


class UserProfile(BaseModel, Entity):
    class Roles(models.TextChoices):
        USER = "U"
        DIETETIC = "D"

    user_id = models.CharField(max_length=255)
    role = models.CharField(
        max_length=3,
        choices=Roles,
        default=Roles.USER,
    )
    website = models.URLField(
        blank=True,
        null=True,
    )
