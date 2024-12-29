from ninja import NinjaAPI

from src.plans.api import router

api = NinjaAPI(
    title="health-manager"
)

api.add_router('/plans/',router)
