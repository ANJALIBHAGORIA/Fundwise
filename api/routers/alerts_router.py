from fastapi import APIRouter

router = APIRouter(prefix="/alerts")

@router.get("/status")
async def status():
    return {"router": "alerts_router", "status": "ok"}
