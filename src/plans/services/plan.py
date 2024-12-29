import typing

from src.core.db import aatomic, aclose_old_connections
from src.plans.models import Plan

if typing.TYPE_CHECKING:
    from src.plans.dto import PlanInputDTO



@aatomic
@aclose_old_connections
async def create(dto: 'PlanInputDTO') -> 'Plan':
    new_plan = Plan(**dto.dict())
    new_plan.full_clean()

    await new_plan.asave()

    return new_plan

async def get_all() -> list['Plan']:
    return await Plan.objects.all()

async def get_by_id(pk: typing.Any) -> 'Plan':
    return await Plan.objects.get(pk=pk)
