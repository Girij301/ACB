from app.repositories.debug_repository import DebugRepository
from app.repositories.execution_repository import ExecutionRepository
from app.repositories.execution_step_repository import (
    ExecutionStepRepository,
)
from app.repositories.retry_repository import RetryRepository
from app.repositories.validation_repository import (
    ValidationRepository,
)


class ExecutionPersistenceService:
    """
    Coordinates persistence repositories used by the
    execution engine.

    This service is intentionally a thin façade.
    Business logic remains inside the execution engine.
    """

    def __init__(
        self,
        execution_repository: ExecutionRepository,
        execution_step_repository: ExecutionStepRepository,
        validation_repository: ValidationRepository,
        retry_repository: RetryRepository,
        debug_repository: DebugRepository,
    ):
        self.execution_repository = execution_repository
        self.execution_step_repository = execution_step_repository
        self.validation_repository = validation_repository
        self.retry_repository = retry_repository
        self.debug_repository = debug_repository