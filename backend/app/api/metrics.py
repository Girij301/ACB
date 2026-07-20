from fastapi import APIRouter

from app.monitoring.execution_metrics import execution_metrics
from app.schemas.base import APIResponse

router = APIRouter(
    tags=["Monitoring"],
)


@router.get(
    "/metrics",
    response_model=APIResponse,
)
def get_metrics():
    """
    Runtime execution metrics.
    """

    snapshot = execution_metrics.snapshot()

    return APIResponse(
        message="Execution metrics retrieved successfully.",
        data=snapshot.model_dump(),
    )
