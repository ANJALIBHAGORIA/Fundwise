from fastapi import APIRouter

router = APIRouter(prefix="/identity")

@router.get("/status")
async def status():
    return {"router": "identity_router", "status": "ok"}
