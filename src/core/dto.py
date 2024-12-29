from ninja import Schema


class BaseOutputDTO(Schema):
    create_time: str
    update_time: str


class BaseMacroDTO(Schema):
    fat: float
    protein: float
    carb: float
    kcal: float


class BaseMacroOutputDTO(BaseOutputDTO, BaseMacroDTO):
    pass
