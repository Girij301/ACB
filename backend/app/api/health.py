from datetime import datetime
from time import perf_counter

from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from app.core.database import SessionLocal, db_dialect
from app.core.logger import logger
from app.docker.docker_manager import DockerManager
from app.schemas.base import APIResponse

router = APIRouter(tags=["Monitoring"])

START_TIME = perf_counter()


@router.get(
    "/health",
    response_model=APIResponse,
)
def health_check():
    """
    Production health endpoint.

    Verifies:
    - Database connectivity
    - Docker availability
    - Application uptime
    """

    logger.info("Health check requested.")

    # --------------------------------------------------
    # Database
    # --------------------------------------------------

    database_status = "healthy"

    try:
        db = SessionLocal()

        db.execute(text("SELECT 1"))

    except Exception:
        logger.exception("Database health check failed.")
        database_status = "unhealthy"

    finally:
        try:
            db.close()
        except Exception:
            pass

    # --------------------------------------------------
    # Docker
    # --------------------------------------------------

    docker_manager = DockerManager()

    docker_available = docker_manager.is_available()

    docker_status = "healthy" if docker_available else "unhealthy"

    # --------------------------------------------------
    # Overall Status
    # --------------------------------------------------

    overall_status = (
        "healthy"
        if database_status == "healthy"
        else "unhealthy"
    )

    payload = {
        "status": overall_status,
        "service": "ACB AI Backend",
        "version": "1.0.0",
        "environment": "development",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "uptime_seconds": round(
            perf_counter() - START_TIME,
            2,
        ),
        "database": {
            "status": database_status,
            "dialect": db_dialect,
        },
        "docker": {
            "enabled": True,
            "status": docker_status,
            "available": docker_available,
        },
    }

    if overall_status != "healthy":
        logger.warning("Health check failed.")

        raise HTTPException(
            status_code=503,
            detail=payload,
        )

    logger.info("Health check completed successfully.")

    return APIResponse(
        message="Health check completed.",
        data=payload,
    )