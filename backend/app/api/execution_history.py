from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_execution_history_service
from app.schemas.execution_history import (
    DebugRecordResponse,
    ExecutionHistoryResponse,
    ExecutionStepResponse,
    RetryRecordResponse,
    ValidationRecordResponse,
)
from app.services.execution_history_service import ExecutionHistoryService

router = APIRouter()


@router.get(
    "/executions",
    response_model=list[ExecutionHistoryResponse],
    tags=["Execution History"],
)
def list_executions(
    history_service: ExecutionHistoryService = Depends(
        get_execution_history_service,
    ),
):
    """
    Return all executions.
    """
    return history_service.list_executions()


@router.get(
    "/executions/{execution_id}",
    response_model=ExecutionHistoryResponse,
    tags=["Execution History"],
)
def get_execution(
    execution_id: int,
    history_service: ExecutionHistoryService = Depends(
        get_execution_history_service,
    ),
):
    """
    Return a single execution.
    """

    execution = history_service.get_execution(execution_id)

    if execution is None:
        raise HTTPException(
            status_code=404,
            detail="Execution not found.",
        )

    return execution


@router.get(
    "/executions/{execution_id}/steps",
    response_model=list[ExecutionStepResponse],
    tags=["Execution History"],
)
def get_execution_steps(
    execution_id: int,
    history_service: ExecutionHistoryService = Depends(
        get_execution_history_service,
    ),
):
    """
    Return execution steps.
    """

    execution = history_service.get_execution(execution_id)

    if execution is None:
        raise HTTPException(
            status_code=404,
            detail="Execution not found.",
        )

    return history_service.get_execution_steps(execution_id)


@router.get(
    "/executions/{execution_id}/validations",
    response_model=list[ValidationRecordResponse],
    tags=["Execution History"],
)
def get_validation_records(
    execution_id: int,
    history_service: ExecutionHistoryService = Depends(
        get_execution_history_service,
    ),
):
    """
    Return validation records.
    """

    execution = history_service.get_execution(execution_id)

    if execution is None:
        raise HTTPException(
            status_code=404,
            detail="Execution not found.",
        )

    return history_service.get_validation_records(execution_id)


@router.get(
    "/executions/{execution_id}/retries",
    response_model=list[RetryRecordResponse],
    tags=["Execution History"],
)
def get_retry_records(
    execution_id: int,
    history_service: ExecutionHistoryService = Depends(
        get_execution_history_service,
    ),
):
    """
    Return retry records.
    """

    execution = history_service.get_execution(execution_id)

    if execution is None:
        raise HTTPException(
            status_code=404,
            detail="Execution not found.",
        )

    return history_service.get_retry_records(execution_id)


@router.get(
    "/executions/{execution_id}/debug",
    response_model=list[DebugRecordResponse],
    tags=["Execution History"],
)
def get_debug_records(
    execution_id: int,
    history_service: ExecutionHistoryService = Depends(
        get_execution_history_service,
    ),
):
    """
    Return debug records.
    """

    execution = history_service.get_execution(execution_id)

    if execution is None:
        raise HTTPException(
            status_code=404,
            detail="Execution not found.",
        )

    return history_service.get_debug_records(execution_id)
