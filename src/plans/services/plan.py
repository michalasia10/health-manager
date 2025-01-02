import typing

from src.core.db import aatomic, aclose_old_connections
from src.plans.models import Plan, PlanRecord
from django.db.models import Q

if typing.TYPE_CHECKING:
    from src.plans.dto import PlanInputDTO


@aclose_old_connections
@aatomic
async def acreate(dto: 'PlanInputDTO') -> 'Plan':
    new_plan = Plan(**dto.dict())
    new_plan.full_clean()

    await new_plan.asave()
    await PlanRecord.create_basic_types(plan=new_plan)

    return new_plan


async def aget_all(query: Q) -> list['Plan']:
    return await Plan.objects.filter(query).all()


async def aget_by_id(pk: typing.Any) -> 'Plan':
    return await Plan.objects.aget(pk=pk)
