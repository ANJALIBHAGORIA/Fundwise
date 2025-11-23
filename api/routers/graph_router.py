"""
graph_router.py
---------------
Graph operations (collusion detection, GNN predictions).
"""

from fastapi import APIRouter
from schemas.user_schema import UserGraphResponse

router = APIRouter(prefix="/graph", tags=["Graph Engine"])

@router.get("/collusion/{user_id}")
async def detect_collusion(user_id: str) -> UserGraphResponse:
    return UserGraphResponse(is_colluding=False, score=0.02)
