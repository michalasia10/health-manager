from datetime import timedelta

import pytest
from faker import Faker

from src.core.exception import ValidationError
from src.plans.dto import PlanInputDTO
from src.plans.models import Plan, PlanRecord, BASIC_TYPES, RecordTypeEnum
from src.plans.services.plan import acreate

pytestmark = [pytest.mark.django_db, pytest.mark.asyncio]
fake = Faker()


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
    assert await PlanRecord.objects.filter(
        plan=plan,
        carb__isnull=False,
        protein__isnull=False,
        fat__isnull=False,
    ).acount() == len(BASIC_TYPES)

    assert isinstance(plan, Plan)
    assert plan.name == dto.name
    assert plan.description == dto.description
    assert plan.is_active


async def test_create_plan_with_records():
    # given
    start_date = fake.date_this_month()

    record_dto = [
        {
            "type": RecordTypeEnum.BREAKFAST,
            "fat": 10.1,
            "protein": 10.1,
            "carb": 10.1,
            "kcal": 150.0,
        },
        {
            "type": RecordTypeEnum.LUNCH,
            "fat": 10.1,
            "protein": 10.1,
            "carb": 10.1,
            "kcal": 150.0,
        },
    ]
    dto_input = {
        "name": "test",
        "description": "test",
        "start_date": start_date,
        "end_date": start_date + timedelta(days=1),
        "fat": 20.2,
        "protein": 20.2,
        "carb": 20.2,
        "kcal": 300.0,
        "records": record_dto,
    }
    dto = PlanInputDTO(**dto_input)

    # when
    plan = await acreate(dto)

    # then
    assert await Plan.objects.aexists()
    assert await PlanRecord.objects.aexists()
    assert await PlanRecord.objects.filter(
        plan=plan,
        carb__isnull=False,
        protein__isnull=False,
        fat__isnull=False,
    ).acount() == len(record_dto)

    assert isinstance(plan, Plan)
    assert plan.name == dto.name
    assert plan.description == dto.description
    assert plan.is_active


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
