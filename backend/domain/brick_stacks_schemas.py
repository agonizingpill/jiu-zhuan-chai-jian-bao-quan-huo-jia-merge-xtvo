from typing import Annotated

from pydantic import BaseModel, ConfigDict, FiniteFloat, StringConstraints

class SurveyStack(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    origin: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    length: FiniteFloat
    perforation: FiniteFloat
    wet: FiniteFloat
    pieces: int


class ConfirmMoisture(BaseModel):
    model_config = ConfigDict(extra="forbid")
    stack: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    wet: FiniteFloat
