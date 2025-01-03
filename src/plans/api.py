from ninja import FilterSchema, Query
from ninja.pagination import paginate
from ninja.router import Router

from src.core.filters import IContainsField
from src.plans.dto import PlanInputDTO, PlanOutputDTO
from src.plans.services.plan import aget_all, acreate, aget_by_id

router = Router(tags=["plans"])


class PlanFilter(FilterSchema):
    name: IContainsField
    description: IContainsField


@router.get("/", response=list[PlanOutputDTO])
@paginate
async def list(request, filters: PlanFilter = Query(...)):
    query = filters.get_filter_expression()
    return await aget_all(query=query)


@router.post("/", response=PlanOutputDTO)
async def create(request, data: PlanInputDTO):
    return await acreate(dto=data)


@router.get("/{pk}", response=PlanOutputDTO)
async def retrieve(request, pk: int):
    return await aget_by_id(pk=pk)
