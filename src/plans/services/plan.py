import typing

from asgiref.sync import sync_to_async
from django.db.models import Q, QuerySet

from src.core.db import safe_aatomic
from src.core.log import log
from src.plans.models import Plan, PlanRecord

if typing.TYPE_CHECKING:
    from src.plans.dto import PlanInputDTO, PlanRecordInputDTO


@safe_aatomic
async def acreate(dto: "PlanInputDTO") -> "Plan":
    clean_dto: dict = dto.dict(exclude_none=True)
    records: list[dict | None] = clean_dto.pop("records", [])

    new_plan = Plan(**clean_dto)

    if not records:
        log("No records provided, creating basic")
        new_records = PlanRecord.create_basic_types(plan=new_plan)
    else:
        new_records = [
            PlanRecord(plan=new_plan, **record).validate() for record in records
        ]

    new_plan.full_clean(records=new_records)
    await new_plan.asave()
    log("Creating plan {new_plan}", new_plan=new_plan)

    new_records = await PlanRecord.objects.abulk_create(new_records)
    new_plan.set_prefetch("records", new_records)

    return new_plan


async def aget_all(query: Q = Q()) -> list["Plan"] | QuerySet["Plan"]:
    return await sync_to_async(
        Plan.objects.filter(query).prefetch_related("records").all
    )()


async def aget_by_id(pk: typing.Any) -> "Plan":
    return await Plan.objects.prefetch_related("records").aget(pk=pk)


@safe_aatomic
async def aadd_record(plan_pk: typing.Any, data: "PlanRecordInputDTO") -> Plan:
    plan = await Plan.objects.prefetch_related("records").aget(pk=plan_pk)

    record = PlanRecord(plan=plan, **data.dict())
    record.full_clean(exclude=["plan"])
    await record.asave()

    log("Adding record {record} to plan {plan}", record=record, plan=plan)

    if await plan.records.aexists():
        records = list(await sync_to_async(plan.records.all)()) + [record]
    else:
        records = [record]

    plan.set_prefetch("records", records)
    return plan


@safe_aatomic
async def aremove_record(pk: typing.Any, record_pk: typing.Any) -> Plan:
    plan = await Plan.objects.prefetch_related("records").aget(pk=pk)

    record = await plan.records.aget(pk=record_pk)

    await record.adelete()

    plan = await Plan.objects.prefetch_related("records").aget(pk=record.plan_id)

    log("Record {record} removed from plan {plan}", record=record_pk, plan=pk)
    return plan
