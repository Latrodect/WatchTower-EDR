from fastapi import APIRouter

from api.endpoints.data import router as data_router
from api.endpoints.security import router as security_router
from api.endpoints.virustotal import router as virustotal_router

router = APIRouter()

router.include_router(virustotal_router)
router.include_router(data_router)
router.include_router(security_router)
