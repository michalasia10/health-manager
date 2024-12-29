from typing import Optional

from src.core.dto import BaseMacroDTO


class PlanInputDTO(BaseMacroDTO):
    name: str
    description: Optional[str] = None
    start_date: str
    end_date: str
