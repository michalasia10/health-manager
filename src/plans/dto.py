from datetime import date
from typing import Optional

from src.core.dto import BaseMacroDTO
from src.plans.models import RecordType


class PlanBaseDTO(BaseMacroDTO):
    name: str
    description: Optional[str] = None
    start_date: date
    end_date: date


class PlanInputDTO(PlanBaseDTO):
    pass


class PlanRecordOutputDTO(BaseMacroDTO):
    type: RecordType


class PlanOutputDTO(PlanBaseDTO):
    is_active: bool
    records: list[PlanRecordOutputDTO]
