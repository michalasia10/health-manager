from enum import Enum

from django.db import models

from src.core.db.models import BaseMacroModel
from src.core.validator.macro import MacroValidator
from src.core.validator.time import DateTimeRangeValidator
from src.plans.validator.plan import PlanMacroSummaryValidator


class Plan(BaseMacroModel):
    VALIDATORS = [
        MacroValidator,
        DateTimeRangeValidator,
        PlanMacroSummaryValidator,
    ]
    # ToDo: Add client field
    # client = models.ForeignKey('clients.Client', on_delete=models.CASCADE)
    # charfield(s)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    # time(s)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    # boolean
    is_active = models.BooleanField(default=True)


class RecordTypeEnum(str, Enum):
    BREAKFAST = "breakfast"
    SNACK = "snack"
    DESSERT = "dessert"
    BRUNCH = "brunch"
    LUNCH = "lunch"
    DINNER = "dinner"


BASIC_TYPES = [
    RecordTypeEnum.BREAKFAST,
    RecordTypeEnum.LUNCH,
    RecordTypeEnum.DINNER,
]


class PlanRecord(BaseMacroModel):
    # relation(s)
    plan = models.ForeignKey(
        to="plans.Plan",
        related_name="records",
        on_delete=models.CASCADE,
    )
    # charfield(s)
    type = models.CharField(
        choices=[
            (RecordTypeEnum.BREAKFAST.value, "Breakfast"),
            (RecordTypeEnum.SNACK.value, "Snack"),
            (RecordTypeEnum.DESSERT.value, "Dessert"),
            (RecordTypeEnum.BRUNCH.value, "Brunch"),
            (RecordTypeEnum.LUNCH.value, "Lunch"),
            (RecordTypeEnum.DINNER.value, "Dinner"),
        ],
        max_length=255,
    )

    @classmethod
    def create_basic_types(cls, plan: Plan) -> list["PlanRecord"]:
        fat = plan.fat / len(BASIC_TYPES)
        protein = plan.protein / len(BASIC_TYPES)
        carb = plan.carb / len(BASIC_TYPES)
        kcal = plan.kcal / len(BASIC_TYPES)

        records = []

        for record_type in BASIC_TYPES:
            record = cls(
                plan=plan,
                type=record_type,
                fat=fat,
                protein=protein,
                carb=carb,
                kcal=kcal,
            )
            record.validate()
            records.append(record)

        return records


class Meal(BaseMacroModel):
    # relation(s)
    record = models.ForeignKey(
        to="plans.PlanRecord",
        related_name="meals",
        on_delete=models.CASCADE,
    )
    # charfield(s)
    name = models.CharField(max_length=255)
