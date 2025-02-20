from typing import Any

from ninja import FilterSchema, Query
from ninja.router import Router

from src.core.api.pagination import default_paginate
from src.core.filters import IContainsField
from src.core.types import RequestT
from src.plans.dto import PlanInputDTO, PlanOutputDTO, PlanRecordInputDTO
from src.plans.services.plan import (
    aget_all,
    acreate,
    aget_by_id,
    aadd_record,
    aremove_record,
)

router = Router(tags=["plans"])


class PlanFilter(FilterSchema):
    name: IContainsField
    description: IContainsField


# ToDo: add patch method(s)


@router.get("/", response=list[PlanOutputDTO], auth=None)
@default_paginate
async def list(request: RequestT, filters: PlanFilter = Query(...)):
    query = filters.get_filter_expression()
    return await aget_all(query=query)


@router.post("/", response=PlanOutputDTO)
async def create(request: RequestT, data: PlanInputDTO):
    return await acreate(dto=data)


@router.get("/{pk}", response=PlanOutputDTO)
async def retrieve(request: RequestT, pk: Any):
    return await aget_by_id(pk=pk)


@router.post("/{pk}/records/add", response=PlanOutputDTO)
async def add_record(request: RequestT, pk: Any, data: PlanRecordInputDTO):
    return await aadd_record(plan_pk=pk, data=data)


@router.delete("/{pk}/records/{record_pk}", response=PlanOutputDTO)
async def delete_record(request: RequestT, pk: Any, record_pk: Any):
    return await aremove_record(pk=pk, record_pk=record_pk)
