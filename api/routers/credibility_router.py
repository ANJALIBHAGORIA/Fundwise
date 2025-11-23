"""
credibility_router.py
---------------------
Compute and retrieve credibility / trust score
"""

from fastapi import APIRouter
from schemas.scoring_schema import CredibilityRequest, CredibilityResponse

router = APIRouter(prefix="/credibility", tags=["Credibility"])

@router.post("/compute")
async def compute_score(req: CredibilityRequest) -> CredibilityResponse:
    return CredibilityResponse(score=0.85, level="green")
