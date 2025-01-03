from datetime import date
from typing import Optional, Any

from src.core.dto import BaseMacroDTO
from src.plans.models import RecordTypeEnum


class PlanBaseDTO(BaseMacroDTO):
    name: str
    description: Optional[str] = None
    start_date: date
    end_date: date


class PlanRecordBaseDTO(BaseMacroDTO):
    type: RecordTypeEnum


class PlanRecordOutputDTO(PlanRecordBaseDTO):
    id: Any


class PlanRecordInputDTO(PlanRecordBaseDTO):
    pass


class PlanInputDTO(PlanBaseDTO):
    records: Optional[list[PlanRecordInputDTO]] = None


class PlanOutputDTO(PlanBaseDTO):
    id: Any
    is_active: bool
    records: list[PlanRecordOutputDTO]
