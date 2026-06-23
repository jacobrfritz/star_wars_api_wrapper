import time
from typing import Any

from fastapi import APIRouter
from star_wars_api_wrapper.config import settings

router = APIRouter()

# Record the start time of the module (approximate service start time)
START_TIME = time.time()


@router.get("/health", status_code=200)
async def health_check() -> dict[str, Any]:
    """
    Checks application health and status.
    Returns general app info and uptime.
    """
    uptime_seconds = time.time() - START_TIME

    return {
        "status": "healthy",
        "environment": settings.ENV,
        "version": settings.APP_VERSION,
        "uptime_seconds": round(uptime_seconds, 2),
    }
