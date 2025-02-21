from src.profiles.models import UserProfile


async def get_or_create_profile(user_id: str) -> UserProfile:
    profile, _ = await UserProfile.objects.aget_or_create(user_id=user_id)
    return profile
