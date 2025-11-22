from fastapi import APIRouter

router = APIRouter(prefix="/credibility")

@router.get("/status")
async def status():
    return {"router": "credibility_router", "status": "ok"}
