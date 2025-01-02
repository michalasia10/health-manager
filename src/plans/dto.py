from datetime import date
from typing import Optional

from src.core.dto import BaseMacroDTO


class PlanBaseDTO(BaseMacroDTO):
    name: str
    description: Optional[str] = None
    start_date: date
    end_date: date


class PlanInputDTO(PlanBaseDTO):
    pass


class PlanOutputDTO(PlanBaseDTO):
    is_active: bool
