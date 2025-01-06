from fastapi import APIRouter

from api.config import AppConfig, get_config
from api.routers.upload import router as upload_router
from api.routers.analytics import router as analytics_router
from api.routers.logs import router as logs_router


router = APIRouter()

router.include_router(analytics_router, prefix="/analytics")
router.include_router(logs_router, prefix="/logs")
router.include_router(upload_router, prefix="/upload")
