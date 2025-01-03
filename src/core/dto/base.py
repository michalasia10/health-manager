from ninja import Schema

from src.core.dto.types import PrecisedFloatAnnotated


class BaseOutputDTO(Schema):
    create_time: str
    update_time: str


class BaseMacroDTO(Schema):
    fat: PrecisedFloatAnnotated
    protein: PrecisedFloatAnnotated
    carb: PrecisedFloatAnnotated
    kcal: PrecisedFloatAnnotated


class BaseMacroOutputDTO(BaseOutputDTO, BaseMacroDTO):
    pass
