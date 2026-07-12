from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.execute import ExecuteRequest
from app.services.execution_manager import execution_manager

router = APIRouter()


@router.post(
    "/execute",
    status_code=status.HTTP_202_ACCEPTED,
)
def execute(
    request: ExecuteRequest,
    db: Session = Depends(get_db),  # kept for future compatibility
):
    """
    Start an execution in the background.

    Returns immediately while the agent continues
    planning and executing asynchronously.
    """

    started = execution_manager.start(request)

    if not started:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An execution is already running for this session.",
        )

    return {
        "success": True,
        "status": "started",
        "message": "Execution started successfully.",
        "session_id": request.session_id,
    }