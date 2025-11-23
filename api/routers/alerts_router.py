"""
alerts_router.py
----------------
Generate rules-based / ML alerts.
"""

from fastapi import APIRouter
from schemas.alert_schema import AlertRequest, AlertResponse

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.post("/trigger")
async def trigger_alert(req: AlertRequest) -> AlertResponse:
    return AlertResponse(status="ok", alerts=[])
