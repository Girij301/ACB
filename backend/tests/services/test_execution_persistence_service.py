from datetime import datetime, timedelta
from types import SimpleNamespace
from unittest.mock import Mock

from app.models.execution import Execution
from app.schemas.execution_status import ExecutionStatus, StepStatus
from app.services.execution_persistence_service import ExecutionPersistenceService


def test_create_execution():
    execution_repository = Mock()
    execution_repository.create.return_value = Execution(
        id=1,
        session_id="session-1",
        plan_id=1,
        status=ExecutionStatus.RUNNING.value,
    )

    service = ExecutionPersistenceService(
        execution_repository=execution_repository,
        execution_step_repository=Mock(),
        validation_repository=Mock(),
        retry_repository=Mock(),
        debug_repository=Mock(),
    )

    execution = service.create_execution(
        session_id="session-1",
        plan_id=1,
    )

    execution_repository.create.assert_called_once()

    created = execution_repository.create.call_args.args[0]

    assert created.session_id == "session-1"
    assert created.plan_id == 1
    assert created.status == ExecutionStatus.RUNNING.value
    assert created.started_at is not None

    assert execution.id == 1


def test_complete_execution():
    repository = Mock()

    repository.update.side_effect = lambda execution: execution

    service = ExecutionPersistenceService(
        execution_repository=repository,
        execution_step_repository=Mock(),
        validation_repository=Mock(),
        retry_repository=Mock(),
        debug_repository=Mock(),
    )

    execution = Execution(
        session_id="session-1",
        plan_id=1,
        status=ExecutionStatus.RUNNING.value,
        started_at=datetime.utcnow() - timedelta(seconds=2),
    )

    completed = service.complete_execution(
        execution=execution,
        success=True,
    )

    repository.update.assert_called_once_with(execution)

    assert completed.status == ExecutionStatus.SUCCESS.value
    assert completed.completed_at is not None
    assert completed.duration_ms >= 2000


def test_record_step():
    step_repository = Mock()
    step_repository.create.side_effect = lambda execution_step: execution_step

    service = ExecutionPersistenceService(
        execution_repository=Mock(),
        execution_step_repository=step_repository,
        validation_repository=Mock(),
        retry_repository=Mock(),
        debug_repository=Mock(),
    )

    execution = Execution(
        id=1,
        session_id="session-1",
        plan_id=1,
        status="RUNNING",
    )

    step = SimpleNamespace(
        step=1,
        action=SimpleNamespace(value="CREATE_FILE"),
        description="Create main.py",
    )

    result = SimpleNamespace(
        status=ExecutionStatus.SUCCESS,
        output={
            "success": True,
            "message": "Created successfully",
        },
    )

    execution_step = service.record_step(
        execution=execution,
        step=step,
        result=result,
    )

    step_repository.create.assert_called_once()

    assert execution_step.execution_id == 1
    assert execution_step.step_index == 1
    assert execution_step.action == "CREATE_FILE"
    assert execution_step.description == "Create main.py"
    assert execution_step.status == StepStatus.SUCCESS.value
    assert execution_step.started_at is not None
    assert execution_step.completed_at is not None
    assert execution_step.duration_ms == 0
    assert execution_step.error is None
    assert execution_step.output is not None


def test_record_validation():
    validation_repository = Mock()
    validation_repository.create.side_effect = lambda record: record

    service = ExecutionPersistenceService(
        execution_repository=Mock(),
        execution_step_repository=Mock(),
        validation_repository=validation_repository,
        retry_repository=Mock(),
        debug_repository=Mock(),
    )

    execution = Execution(
        id=1,
        session_id="session-1",
        plan_id=1,
        status="RUNNING",
    )

    validation_result = SimpleNamespace(
        validator="ruff",
        success=True,
        stdout="All checks passed",
        stderr=None,
        duration_ms=125,
    )

    record = service.record_validation(
        execution=execution,
        validation_result=validation_result,
    )

    validation_repository.create.assert_called_once()

    assert record.execution_id == 1
    assert record.validator_name == "ruff"
    assert record.passed is True
    assert record.stdout == "All checks passed"
    assert record.stderr is None
    assert record.duration_ms == 125


def test_record_retry():
    retry_repository = Mock()
    retry_repository.create.side_effect = lambda record: record

    service = ExecutionPersistenceService(
        execution_repository=Mock(),
        execution_step_repository=Mock(),
        validation_repository=Mock(),
        retry_repository=retry_repository,
        debug_repository=Mock(),
    )

    execution = Execution(
        id=1,
        session_id="session-1",
        plan_id=1,
        status="RUNNING",
    )

    step = SimpleNamespace(
        step=2,
    )

    analysis = SimpleNamespace(
        reason="Temporary failure",
    )

    record = service.record_retry(
        execution=execution,
        step=step,
        retry_attempt=1,
        analysis=analysis,
        previous_error="File not found",
        success=False,
    )

    retry_repository.create.assert_called_once()

    assert record.execution_id == 1
    assert record.step_index == 2
    assert record.attempt_number == 1
    assert record.reason == "Temporary failure"
    assert record.previous_error == "File not found"
    assert record.success is False


def test_record_debug():
    debug_repository = Mock()
    debug_repository.create.side_effect = lambda record: record

    service = ExecutionPersistenceService(
        execution_repository=Mock(),
        execution_step_repository=Mock(),
        validation_repository=Mock(),
        retry_repository=Mock(),
        debug_repository=debug_repository,
    )

    execution = Execution(
        id=1,
        session_id="session-1",
        plan_id=1,
        status="RUNNING",
    )

    step = SimpleNamespace(
        step=1,
    )

    record = service.record_debug(
        execution=execution,
        step=step,
        attempt_number=1,
        failure_summary="Syntax error in main.py",
        ai_summary="Added missing colon",
        success=True,
    )

    debug_repository.create.assert_called_once()

    assert record.execution_id == 1
    assert record.step_index == 1
    assert record.attempt_number == 1
    assert record.failure_summary == "Syntax error in main.py"
    assert record.ai_summary == "Added missing colon"
    assert record.success is True
