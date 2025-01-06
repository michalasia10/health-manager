from datetime import timedelta

import pytest
from faker import Faker

from src.core.exception import ValidationError
from src.plans.dto import PlanInputDTO, PlanRecordInputDTO
from src.plans.models import Plan, PlanRecord, BASIC_TYPES, RecordTypeEnum
from src.plans.services.plan import (
    acreate,
    aadd_record,
    aremove_record,
    aget_all,
    aget_by_id,
)

pytestmark = [pytest.mark.django_db, pytest.mark.asyncio]
fake = Faker()


@pytest.mark.django_db(transaction=True)
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


@pytest.mark.django_db(transaction=True)
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


async def test_get_all_plans(basic_plan):
    # when
    plans = await aget_all()

    # then
    assert await plans.acount() == 1


async def test_get_plan_by_id(basic_plan):
    # when
    plan = await aget_by_id(pk=basic_plan.pk)

    # then
    assert plan
    assert plan.pk == basic_plan.pk


async def test_add_record_to_plan_without_records(basic_plan):
    # sanity check
    assert await Plan.objects.filter(id=basic_plan.pk).aexists()
    assert not await PlanRecord.objects.filter(plan=basic_plan).aexists()

    # given
    dto_input = {
        "type": RecordTypeEnum.BREAKFAST,
        "fat": 20.2,
        "protein": 20.2,
        "carb": 20.2,
        "kcal": 300.0,
    }
    dto = PlanRecordInputDTO(**dto_input)

    # when
    plan = await aadd_record(plan_pk=basic_plan.pk, data=dto)

    # then
    assert (
        await PlanRecord.objects.filter(
            plan=plan,
            carb__isnull=False,
            protein__isnull=False,
            fat__isnull=False,
        ).acount()
        == 1
    )


async def test_add_record_to_unexisting_plan():
    # given
    dto_input = {
        "type": RecordTypeEnum.BREAKFAST,
        "fat": 20.2,
        "protein": 20.2,
        "carb": 20.2,
        "kcal": 300.0,
    }
    dto = PlanRecordInputDTO(**dto_input)

    # when
    with pytest.raises(Plan.DoesNotExist):
        await aadd_record(plan_pk=fake.randomize_nb_elements(number=2000), data=dto)


async def test_add_record_to_plan_with_records(plan_with_record):
    # sanity check
    assert await Plan.objects.filter(id=plan_with_record.pk).aexists()
    assert await PlanRecord.objects.filter(plan=plan_with_record).aexists()

    # given
    dto_input = {
        "type": RecordTypeEnum.BREAKFAST,
        "fat": 20.2,
        "protein": 20.2,
        "carb": 20.2,
        "kcal": 300.0,
    }
    dto = PlanRecordInputDTO(**dto_input)

    # when
    plan = await aadd_record(plan_pk=plan_with_record.pk, data=dto)

    # then
    assert (
        await PlanRecord.objects.filter(
            plan=plan,
            carb__isnull=False,
            protein__isnull=False,
            fat__isnull=False,
        ).acount()
        == 2
    )


async def test_remove_record_from_plan(plan_with_record):
    # sanity check
    assert await Plan.objects.filter(id=plan_with_record.pk).aexists()
    assert await PlanRecord.objects.filter(plan=plan_with_record).aexists()

    # given
    record = await plan_with_record.records.afirst()

    # when
    plan = await aremove_record(pk=plan_with_record.pk, record_pk=record.pk)

    # then
    assert (
        await PlanRecord.objects.filter(
            plan=plan,
            carb__isnull=False,
            protein__isnull=False,
            fat__isnull=False,
        ).acount()
        == 0
    )
