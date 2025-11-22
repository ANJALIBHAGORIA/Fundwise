from fastapi import APIRouter

router = APIRouter(prefix="/anomaly")

@router.get("/status")
async def status():
    return {"router": "anomaly_router", "status": "ok"}
