from typing import Optional
from pydantic import BaseModel


class FactCheckAPIResponse(BaseModel):
    is_correct: str
    explanations: str
    sources: list[str]
    claim: str
    corrected_claim: str


class FactCheckResponse(BaseModel):
    text: str
    accuracy: float
    false_information: Optional[list[FactCheckAPIResponse]] = None
    status: bool
