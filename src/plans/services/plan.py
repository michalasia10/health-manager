import typing

import logfire
from django.db.models import Q

from src.core.db import aatomic, aclose_old_connections
from src.plans.models import Plan, PlanRecord

if typing.TYPE_CHECKING:
    from src.plans.dto import PlanInputDTO


@aclose_old_connections
@aatomic
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
    return await Plan.objects.filter(query).all()


async def aget_by_id(pk: typing.Any) -> "Plan":
    return await Plan.objects.aget(pk=pk)
