from datetime import UTC, datetime

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
from app.schemas.execution_status import ExecutionStatus, StepStatus


class ExecutionPersistenceService:
    """
    Coordinates persistence operations used by the
    execution engine.

    This service provides a clean interface for the
    execution engine while delegating database access
    to the repository layer.
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

    def create_execution(
        self,
        session_id: str,
        plan_id: int,
    ) -> Execution:
        """
        Create a new execution record when an execution starts.
        """

        execution = Execution(
            session_id=session_id,
            plan_id=plan_id,
            status=ExecutionStatus.RUNNING.value,
            started_at=datetime.now(UTC),
        )

        return self.execution_repository.create(execution)

    def complete_execution(
        self,
        execution: Execution,
        success: bool,
    ) -> Execution:
        """
        Mark an execution as completed and persist
        the final execution metadata.
        """

        completed_at = datetime.now(UTC)

        execution.completed_at = completed_at

        if execution.started_at is not None:
            execution.duration_ms = int(
                (completed_at - execution.started_at).total_seconds() * 1000
            )

        execution.status = (
            ExecutionStatus.SUCCESS.value if success else ExecutionStatus.FAILED.value
        )

        return self.execution_repository.update(execution)

    def record_step(
        self,
        execution: Execution,
        step,
        result,
    ) -> ExecutionStep:
        """
        Persist a single execution step.
        """

        now = datetime.now(UTC)

        execution_step = ExecutionStep(
            execution_id=execution.id,
            step_index=step.step,
            action=step.action.value,
            description=step.description,
            status=(
                StepStatus.SUCCESS.value
                if result.status.name == "SUCCESS"
                else StepStatus.FAILED.value
            ),
            tool_name=None,
            output=getattr(result, "output", None),
            error=result.error,
            duration_ms=0,
            started_at=now,
            completed_at=now,
        )

        return self.execution_step_repository.create(execution_step)

    def record_validation(
        self,
        execution: Execution,
        validation_result,
    ) -> ValidationRecord:
        """
        Persist a validation result.
        """

        record = ValidationRecord(
            execution_id=execution.id,
            validator_name=validation_result.validator,
            passed=validation_result.success,
            stdout=getattr(validation_result, "stdout", None),
            stderr=getattr(validation_result, "stderr", None),
            duration_ms=getattr(validation_result, "duration_ms", 0),
        )

        return self.validation_repository.create(record)

    def record_retry(
        self,
        execution: Execution,
        step,
        retry_attempt: int,
        analysis,
        previous_error: str | None,
        success: bool,
    ) -> RetryRecord:
        """
        Persist a retry attempt.
        """

        retry_record = RetryRecord(
            execution_id=execution.id,
            step_index=step.step,
            attempt_number=retry_attempt,
            reason=analysis.reason,
            previous_error=previous_error,
            success=success,
        )

        return self.retry_repository.create(retry_record)

    def record_debug(
        self,
        execution: Execution,
        step,
        attempt_number: int,
        failure_summary: str,
        ai_summary: str | None,
        success: bool,
    ) -> DebugRecord:
        """
        Persist an AI debugging attempt.
        """

        debug_record = DebugRecord(
            execution_id=execution.id,
            step_index=step.step,
            attempt_number=attempt_number,
            failure_summary=failure_summary,
            ai_summary=ai_summary,
            success=success,
        )

        return self.debug_repository.create(debug_record)
