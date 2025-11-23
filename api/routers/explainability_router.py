"""
explainability_router.py
------------------------
Provides human-readable reasoning behind ML outputs.
"""

from fastapi import APIRouter
from schemas.scoring_schema import ExplainabilityResponse

router = APIRouter(prefix="/explain", tags=["Explainability"])

@router.get("/trustscore/{user_id}")
async def explain_score(user_id: str) -> ExplainabilityResponse:
    return ExplainabilityResponse(
        explanation="Low velocity + stable device + clean graph"
    )
