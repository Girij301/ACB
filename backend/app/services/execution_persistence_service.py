import json
from datetime import datetime

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
from app.schemas.execution import ExecutionSummary
from app.schemas.execution_status import (
    ExecutionStatus,
    StepExecutionStatus,
    StepStatus,
)


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

    def build_execution_summary(
        self,
        execution: Execution,
        workspace: str,
    ) -> ExecutionSummary:
        """
        Convert an Execution model into an API response model.
        """

        return ExecutionSummary(
            execution_id=execution.id,
            session_id=execution.session_id,
            plan_id=execution.plan_id,
            status=execution.status,
            workspace=workspace,
            total_steps=execution.total_steps,
            successful_steps=execution.successful_steps,
            failed_steps=execution.failed_steps,
            retry_count=execution.retry_count,
            debug_count=execution.debug_count,
            validation_count=execution.validation_count,
            duration_ms=execution.duration_ms,
            started_at=execution.started_at,
            completed_at=execution.completed_at,
        )

    def create_execution(
        self,
        session_id: str,
        plan_id: int,
        total_steps: int,
    ) -> Execution:
        """
        Create a new execution record when an execution starts.
        """

        execution = Execution(
            session_id=session_id,
            plan_id=plan_id,
            status=ExecutionStatus.RUNNING.value,
            started_at=datetime.utcnow(),
            total_steps=total_steps,
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

        completed_at = datetime.utcnow()

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

        if result.status == StepExecutionStatus.SUCCESS:
            execution.successful_steps += 1
        else:
            execution.failed_steps += 1

        self.execution_repository.update(execution)

        now = datetime.utcnow()

        output = getattr(result, "output", None)

        execution_step = ExecutionStep(
            execution_id=execution.id,
            step_index=step.step,
            action=step.action.value,
            description=step.description,
            status=(
                StepStatus.SUCCESS.value
                if result.status == StepExecutionStatus.SUCCESS
                else StepStatus.FAILED.value
            ),
            tool_name=None,
            output=(json.dumps(output, indent=2) if output is not None else None),
            error=(output.get("error") if isinstance(output, dict) else None),
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

        execution.validation_count += 1
        self.execution_repository.update(execution)

        record = ValidationRecord(
            execution_id=execution.id,
            validator_name=validation_result.validator,
            passed=validation_result.success,
            stdout=getattr(
                validation_result,
                "stdout",
                None,
            ),
            stderr=getattr(
                validation_result,
                "stderr",
                None,
            ),
            duration_ms=getattr(
                validation_result,
                "duration_ms",
                0,
            ),
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

        execution.retry_count += 1
        self.execution_repository.update(execution)

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

        execution.debug_count += 1
        self.execution_repository.update(execution)

        debug_record = DebugRecord(
            execution_id=execution.id,
            step_index=step.step,
            attempt_number=attempt_number,
            failure_summary=failure_summary,
            ai_summary=ai_summary,
            success=success,
        )

        return self.debug_repository.create(debug_record)
