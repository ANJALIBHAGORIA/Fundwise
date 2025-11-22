from fastapi import APIRouter

router = APIRouter(prefix="/dashboard")

@router.get("/status")
async def status():
    return {"router": "dashboard_router", "status": "ok"}
