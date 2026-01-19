from pydantic import BaseModel
from typing import List


class FactorContribution(BaseModel):
    factor: str
    value: float
    weight: float
    impact: str  # low | medium | high


class RiskExplanation(BaseModel):
    risk_score: float
    primary_driver: str
    contributors: List[FactorContribution]
    trend: str
    summary: str
