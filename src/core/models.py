from django.db import models


class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.__class__.__name__}_{self.pk}"


class BaseMacroModel(BaseModel):
    fat = models.FloatField()
    protein = models.FloatField()
    carb = models.FloatField()
    kcal = models.FloatField()

    class Meta:
        abstract = True
