from datetime import timedelta

import pytest
from django.core.exceptions import ValidationError
from faker import Faker

from src.plans.dto import PlanInputDTO
from src.plans.models import Plan, PlanRecord, BASIC_TYPES
from src.plans.services.plan import acreate

pytestmark = pytest.mark.django_db
fake = Faker()


@pytest.mark.asyncio
async def test_create_plan():
    # given
    start_date = fake.date_this_month()

    dto_input = {
        "name": "test",
        "description": "test",
        "start_date": start_date,
        "end_date": start_date + timedelta(days=1),
        "fat": 20.2,
        "protein": 20.2,
        "carb": 20.2,
        "kcal": 300.0,

    }
    dto = PlanInputDTO(**dto_input)

    # when
    plan = await acreate(dto)

    # then
    assert await Plan.objects.aexists()
    assert await PlanRecord.objects.aexists()
    assert await PlanRecord.objects.filter(plan=plan).acount() == len(BASIC_TYPES)

    assert isinstance(plan, Plan)
    assert plan.name == dto.name
    assert plan.description == dto.description
    assert plan.is_active


@pytest.mark.asyncio
async def test_create_plan_with_invalid_end_date():
    # given
    start_date = fake.date_this_month()

    dto_input = {
        "name": "test",
        "description": "test",
        "start_date": start_date,
        "end_date": start_date - timedelta(days=1),
        "fat": 20.2,
        "protein": 20.2,
        "carb": 20.2,
        "kcal": 300.0,
    }
    dto = PlanInputDTO(**dto_input)

    # when
    with pytest.raises(ValidationError):
        await acreate(dto)
