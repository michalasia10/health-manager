from functools import lru_cache, cached_property
from typing import Any

from asgiref.sync import sync_to_async
from django.conf import settings
from openfoodfacts import API, Environment
from pydantic import BaseModel, Field

from src.core.dto import PrecisedFloatAnnotated
from src.core.log import log


class Macro(BaseModel):
    kcal: PrecisedFloatAnnotated = Field(alias="energy-kcal_100g")
    fat: PrecisedFloatAnnotated = Field(alias="fat_100g")
    carb: PrecisedFloatAnnotated = Field(alias="carbohydrates_100g")
    protein: PrecisedFloatAnnotated = Field(alias="proteins_100g")


class Product(BaseModel):
    name: str = Field(..., alias="product_name")
    macro: Macro = Field(..., alias="nutriments")


@lru_cache
def get_food_api_client() -> API:
    return API(
        user_agent=settings.OPEN_FOOD_AGENT,
        timeout=5,
        username=settings.OPEN_FOOD_LOGIN,
        password=settings.OPEN_FOOD_PASSWORD,
        environment=Environment.net,
    )


class FoodApiClient:
    @cached_property
    def _client(self) -> API:
        return get_food_api_client()

    async def search_product(
        self, query: str, offset: int = 0, limit: int = 10
    ) -> dict[str, list[dict] | Any]:
        try:
            return await sync_to_async(self._client.product.text_search)(
                query=query,
                page_size=limit,
                page=offset + 1,
            )
        except Exception as e:
            log(
                "Error searching product {query}: {e}",
                level="warning",
                query=query,
                e=e,
            )
            return dict(products=[])


@lru_cache
def get_internal_food_api_client() -> FoodApiClient:
    return FoodApiClient()


class MealSearchService:
    @cached_property
    def _client(self) -> FoodApiClient:
        return get_internal_food_api_client()

    async def search(self, query: str, offset: int = 0, limit: int = 20):
        result = await self._client.search_product(
            query=query.name, offset=offset, limit=limit
        )
        products = [
            product
            for product in result.get("products", [])
            if product.get("nutriments", {})
        ]

        # breakpoint()
        if products:
            return dict(
                missing_count=limit - len(products),
                limit=limit,
                offset=offset,
                count=len(products),
                items=[Product.model_validate(product) for product in products],
            )

        return dict(missing_count=limit, limit=limit, offset=offset, count=0, items=[])
