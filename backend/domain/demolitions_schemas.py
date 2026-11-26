from typing import Annotated

from pydantic import BaseModel, ConfigDict, FiniteFloat, StringConstraints

class ConfirmRelease(BaseModel):
    model_config = ConfigDict(extra="forbid")
    origin: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    allowed: bool
