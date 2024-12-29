from django.db import models

from src.core.models import BaseMacroModel


class Plan(BaseMacroModel):
    # ToDo: Add client field
    # client = models.ForeignKey('clients.Client', on_delete=models.CASCADE)
    # charfield(s)
    name = models.CharField(max_length=255)
    description = models.TextField()
    # time(s)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    # boolean
    is_active = models.BooleanField(default=True)


class PlanRecord(BaseMacroModel):
    # relation(s)
    plan = models.ForeignKey(
        to='plans.Plan',
        related_name='records',
        on_delete=models.CASCADE,
    )
    # charfield(s)
    type = models.CharField(
        choices=[
            ('breakfast', 'Breakfast'),
            ('snack', 'Snack'),
            ('dessert', 'Dessert'),
            ('brunch', 'Brunch'),
            ('lunch', 'Lunch'),
            ('dinner', 'Dinner'),
        ],
        max_length=255
    )


class Meal(BaseMacroModel):
    # relation(s)
    record = models.ForeignKey(
        to='plans.PlanRecord',
        related_name='meals',
        on_delete=models.CASCADE,
    )
    # charfield(s)
    name = models.CharField(max_length=255)
