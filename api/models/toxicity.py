from typing import List, Optional
from pydantic import BaseModel
import numpy as np


class ToxicityEvaluationResult(BaseModel):
    toxicity: np.float32
    severe_toxicity: np.float32
    obscene: np.float32
    identity_attack: np.float32
    insult: np.float32
    threat: np.float32
    sexual_explicit: np.float32


class ToxicityLabel(BaseModel):
    label: str
    score: float


class ToxicityResult(BaseModel):
    status: bool
    reason: str
    labels: Optional[List[ToxicityLabel]]
