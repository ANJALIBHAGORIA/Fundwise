from fastapi import APIRouter

router = APIRouter(prefix="/explainability")

@router.get("/status")
async def status():
    return {"router": "explainability_router", "status": "ok"}
