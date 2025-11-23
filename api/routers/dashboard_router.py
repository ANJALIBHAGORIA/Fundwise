"""
dashboard_router.py
-------------------
Aggregated metrics for groups and fund cycles.
"""

from fastapi import APIRouter
from schemas.dashboard_schema import DashboardResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/group/{group_id}")
async def get_group_dashboard(group_id: str) -> DashboardResponse:
    return DashboardResponse(group_id=group_id, transparency_score=0.91)
