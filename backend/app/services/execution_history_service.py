from app.models.debug_record import DebugRecord
from app.models.execution import Execution
from app.models.execution_step import ExecutionStep
from app.models.retry_record import RetryRecord
from app.models.validation_record import ValidationRecord
from app.repositories.debug_repository import DebugRepository
from app.repositories.execution_repository import ExecutionRepository
from app.repositories.execution_step_repository import ExecutionStepRepository
from app.repositories.retry_repository import RetryRepository
from app.repositories.validation_repository import ValidationRepository


class ExecutionHistoryService:
    """
    Provides read-only access to execution history.

    This service coordinates repository queries while
    keeping all database access inside the repository
    layer.
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

    def list_executions(self) -> list[Execution]:
        """
        Return all executions ordered from newest
        to oldest.
        """
        return self.execution_repository.list()

    def get_execution(
        self,
        execution_id: int,
    ) -> Execution | None:
        """
        Return a single execution by its id.
        """
        return self.execution_repository.get_by_id(execution_id)

    def get_execution_steps(
        self,
        execution_id: int,
    ) -> list[ExecutionStep]:
        """
        Return all execution steps for an execution.
        """
        return self.execution_step_repository.list_by_execution(execution_id)

    def get_validation_records(
        self,
        execution_id: int,
    ) -> list[ValidationRecord]:
        """
        Return all validation records for an execution.
        """
        return self.validation_repository.list_by_execution(execution_id)

    def get_retry_records(
        self,
        execution_id: int,
    ) -> list[RetryRecord]:
        """
        Return all retry records for an execution.
        """
        return self.retry_repository.list_by_execution(execution_id)

    def get_debug_records(
        self,
        execution_id: int,
    ) -> list[DebugRecord]:
        """
        Return all debug records for an execution.
        """
        return self.debug_repository.list_by_execution(execution_id)
