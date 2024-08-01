from fastapi import APIRouter

router = APIRouter()

@router.get("/status")
async def security_status():
    return {"status": "Security is operational"}
