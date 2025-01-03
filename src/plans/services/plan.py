import typing

import logfire
from asgiref.sync import sync_to_async
from django.db.models import Q

from src.core.db import aatomic, aclose_old_connections, safe_aatomic
from src.plans.models import Plan, PlanRecord

if typing.TYPE_CHECKING:
    from src.plans.dto import PlanInputDTO, PlanRecordInputDTO


@safe_aatomic
async def acreate(dto: "PlanInputDTO") -> "Plan":
    clean_dto: dict = dto.dict(exclude_none=True)
    records: list[dict | None] = clean_dto.pop("records", [])

    new_plan = Plan(**clean_dto)
    new_plan.full_clean()

    await new_plan.asave()
    logfire.info("Creating plan {new_plan}", new_plan=new_plan)

    if not records:
        logfire.info("No records provided, creating basic")
        await PlanRecord.create_basic_types(plan=new_plan)

    for record in records:
        new_record = PlanRecord(plan=new_plan, **record)
        new_record.full_clean(exclude=["plan"])
        await new_record.asave()

    return new_plan


async def aget_all(query: Q) -> list["Plan"]:
    return await sync_to_async(lambda: Plan.objects.filter(query).prefetch_related('records').all())()


async def aget_by_id(pk: typing.Any) -> "Plan":
    return await Plan.objects.aget(pk=pk)

@safe_aatomic
async def aadd_record(plan_pk: int, data: "PlanRecordInputDTO") -> PlanRecord:
    plan = await Plan.objects.prefetch_related('records').aget(pk=plan_pk)

    record = PlanRecord(plan=plan, **data.dict())
    record.full_clean(exclude=["plan"])
    await record.asave()

    logfire.info("Adding record {record} to plan {plan}", record=record, plan=plan)

    plan.set_prefetch("records", plan + [record])
    return plan


@safe_aatomic
async def aremove_record(pk: typing.Any) -> PlanRecord:
    record = await PlanRecord.objects.select_related('plan').aget(pk=pk)

    await record.adelete()
    plan = await Plan.objects.prefetch_related('records').aget(pk=record.plan_id)

    logfire.info("Record {record} removed from plan {plan}", record=pk, plan=plan)
    return plan
