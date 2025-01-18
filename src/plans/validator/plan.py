import typing

from src.core.const import MACRO_ATTRS
from src.core.exception import DomainError
from src.core.validator.base import Validator

if typing.TYPE_CHECKING:
    from src.plans.models import Plan, PlanRecord


class PlanMacroSummaryValidator(Validator):
    def validate(self, records: typing.Optional[list["PlanRecord"]] = None) -> None:
        if not records:
            return

        self.model_instance: "Plan"

        for macro in MACRO_ATTRS:
            plan_value = getattr(self.model_instance, macro)
            sum_value = sum([getattr(record, macro) for record in records])

            if sum_value > plan_value:
                raise DomainError(
                    f"Sum of {macro} in records must be less than or equal to {macro} in plan.",
                    extra=dict(sum_value=sum_value, plan_value=plan_value),
                )

            if plan_value != sum_value:
                raise DomainError(
                    f"Sum of {macro} in records must be equal to {macro} in plan.",
                    extra=dict(sum_value=sum_value, plan_value=plan_value),
                )
