from datetime import UTC, datetime
from unittest.mock import Mock

from app.models.debug_record import DebugRecord
from app.models.execution import Execution
from app.models.execution_step import ExecutionStep
from app.models.retry_record import RetryRecord
from app.models.validation_record import ValidationRecord
from app.services.execution_history_service import ExecutionHistoryService


def test_list_executions():
    execution_repository = Mock()

    executions = [
        Execution(
            id=1,
            session_id="session-1",
            plan_id=1,
            status="RUNNING",
            started_at=datetime.now(UTC),
        ),
        Execution(
            id=2,
            session_id="session-2",
            plan_id=2,
            status="RUNNING",
            started_at=datetime.now(UTC),
        ),
    ]

    execution_repository.list.return_value = executions

    service = ExecutionHistoryService(
        execution_repository=execution_repository,
        execution_step_repository=Mock(),
        validation_repository=Mock(),
        retry_repository=Mock(),
        debug_repository=Mock(),
    )

    result = service.list_executions()

    execution_repository.list.assert_called_once()

    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2


def test_get_execution():
    execution_repository = Mock()

    execution = Execution(
        id=10,
        session_id="session-1",
        plan_id=1,
        status="RUNNING",
        started_at=datetime.now(UTC),
    )

    execution_repository.get_by_id.return_value = execution

    service = ExecutionHistoryService(
        execution_repository=execution_repository,
        execution_step_repository=Mock(),
        validation_repository=Mock(),
        retry_repository=Mock(),
        debug_repository=Mock(),
    )

    result = service.get_execution(10)

    execution_repository.get_by_id.assert_called_once_with(10)

    assert result is execution


def test_get_execution_steps():
    step_repository = Mock()

    steps = [
        ExecutionStep(
            execution_id=1,
            step_index=1,
            action="CREATE_FILE",
            description="Create main.py",
            status="SUCCESS",
            started_at=datetime.now(UTC),
        )
    ]

    step_repository.list_by_execution.return_value = steps

    service = ExecutionHistoryService(
        execution_repository=Mock(),
        execution_step_repository=step_repository,
        validation_repository=Mock(),
        retry_repository=Mock(),
        debug_repository=Mock(),
    )

    result = service.get_execution_steps(1)

    step_repository.list_by_execution.assert_called_once_with(1)

    assert len(result) == 1
    assert result[0].step_index == 1


def test_get_validation_records():
    validation_repository = Mock()

    records = [
        ValidationRecord(
            execution_id=1,
            validator_name="ruff",
            passed=True,
        )
    ]

    validation_repository.list_by_execution.return_value = records

    service = ExecutionHistoryService(
        execution_repository=Mock(),
        execution_step_repository=Mock(),
        validation_repository=validation_repository,
        retry_repository=Mock(),
        debug_repository=Mock(),
    )

    result = service.get_validation_records(1)

    validation_repository.list_by_execution.assert_called_once_with(1)

    assert len(result) == 1
    assert result[0].validator_name == "ruff"


def test_get_retry_records():
    retry_repository = Mock()

    records = [
        RetryRecord(
            execution_id=1,
            step_index=1,
            attempt_number=1,
            reason="Command failed",
            success=True,
        )
    ]

    retry_repository.list_by_execution.return_value = records

    service = ExecutionHistoryService(
        execution_repository=Mock(),
        execution_step_repository=Mock(),
        validation_repository=Mock(),
        retry_repository=retry_repository,
        debug_repository=Mock(),
    )

    result = service.get_retry_records(1)

    retry_repository.list_by_execution.assert_called_once_with(1)

    assert len(result) == 1
    assert result[0].attempt_number == 1


def test_get_debug_records():
    debug_repository = Mock()

    records = [
        DebugRecord(
            execution_id=1,
            step_index=1,
            attempt_number=1,
            failure_summary="Compilation failed",
            success=True,
        )
    ]

    debug_repository.list_by_execution.return_value = records

    service = ExecutionHistoryService(
        execution_repository=Mock(),
        execution_step_repository=Mock(),
        validation_repository=Mock(),
        retry_repository=Mock(),
        debug_repository=debug_repository,
    )

    result = service.get_debug_records(1)

    debug_repository.list_by_execution.assert_called_once_with(1)

    assert len(result) == 1
    assert result[0].failure_summary == "Compilation failed"
