from fastapi import APIRouter

router = APIRouter(prefix="/escrow")

@router.get("/status")
async def status():
    return {"router": "escrow_router", "status": "ok"}
