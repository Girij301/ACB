from app.core.database import get_db
from app.repositories.debug_repository import DebugRepository
from app.repositories.execution_repository import ExecutionRepository
from app.repositories.execution_step_repository import ExecutionStepRepository
from app.repositories.retry_repository import RetryRepository
from app.repositories.validation_repository import ValidationRepository
from app.services.execution_history_service import ExecutionHistoryService
from fastapi import Depends
from sqlalchemy.orm import Session


def get_execution_history_service(
    db: Session = Depends(get_db),
) -> ExecutionHistoryService:
    """
    Dependency that provides an ExecutionHistoryService
    with all required repositories.
    """

    return ExecutionHistoryService(
        execution_repository=ExecutionRepository(db),
        execution_step_repository=ExecutionStepRepository(db),
        validation_repository=ValidationRepository(db),
        retry_repository=RetryRepository(db),
        debug_repository=DebugRepository(db),
    )
