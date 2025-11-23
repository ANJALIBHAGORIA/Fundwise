"""
scoring_schema.py
-----------------
Credibility score & explanation models
"""

from pydantic import BaseModel
from typing import Dict

class CredibilityRequest(BaseModel):
    user_id: str

class CredibilityResponse(BaseModel):
    score: float
    level: str

class ExplainabilityResponse(BaseModel):
    explanation: str
