from typing import Annotated

from pydantic import BaseModel, ConfigDict, FiniteFloat, StringConstraints

class PackRack(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    candidate: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    rack: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    operator_note: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
