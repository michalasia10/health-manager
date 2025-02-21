import pytest_asyncio
from asgiref.sync import sync_to_async
from model_bakery import baker


@pytest_asyncio.fixture
async def profile():
    return await sync_to_async(baker.make)(
        "profiles.UserProfile", _refresh_after_create=True
    )
