import pytest
from faker import Faker

from src.profiles.models import UserProfile
from src.profiles.service import get_or_create_profile

pytestmark = [pytest.mark.django_db, pytest.mark.asyncio]
fake = Faker()


async def test_get_profile_if_exists(profile: UserProfile):
    # when
    actual_profile = await get_or_create_profile(profile.user_id)

    # then
    assert actual_profile == profile


async def test_create_profile_if_not_exists(profile: UserProfile):
    # when
    new_profile = await get_or_create_profile(fake.name())

    # then
    assert new_profile != profile
