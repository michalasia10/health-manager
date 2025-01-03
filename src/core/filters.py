from typing import Annotated, Optional

from pydantic import Field

IContainsField = Annotated[Optional[str], Field(None, q="__icontains")]
