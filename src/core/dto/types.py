from pydantic import AfterValidator
from typing_extensions import Annotated

from src.core.value_object import PrecisedFloat

PrecisedFloatAnnotated = Annotated[float, AfterValidator(PrecisedFloat)]
