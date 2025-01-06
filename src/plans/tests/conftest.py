import pytest_asyncio
from model_bakery import baker, random_gen
from asgiref.sync import sync_to_async

baker.generators.add("src.core.db.fields.PrecisedFloatField", random_gen.gen_float)


@pytest_asyncio.fixture()
async def basic_plan():
    return await sync_to_async(baker.make)("plans.Plan", _refresh_after_create=True)


@pytest_asyncio.fixture
async def plan_with_record(basic_plan):
    await sync_to_async(baker.make)(
        "plans.PlanRecord", plan=basic_plan, _refresh_after_create=True
    )
    return basic_plan
