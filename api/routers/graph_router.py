from fastapi import APIRouter

router = APIRouter(prefix="/graph")

@router.get("/status")
async def status():
    return {"router": "graph_router", "status": "ok"}
