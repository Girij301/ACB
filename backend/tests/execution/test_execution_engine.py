from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

from app.execution.context import ExecutionContext
from app.execution.engine import ExecutionEngine
from app.models.execution import Execution
from app.schemas.execution import ExecutionStatus, StepResult
from app.schemas.validation import ValidationResult
from app.schemas.validation_execution import ValidationExecutionResult


class FakeStepExecutor:
    def execute(self, step, context):
        return StepResult(
            step_number=step.step,
            description=step.description,
            status=ExecutionStatus.SUCCESS,
            message="Success",
            output={},
        )


class SuccessValidationEngine:
    def __init__(self):
        self.called = False

    def validate(self, context, history):
        self.called = True

        return ValidationExecutionResult(
            success=True,
            attempts=1,
            results=[
                ValidationResult(
                    success=True,
                    validator="ruff",
                    message="Passed",
                )
            ],
        )


class FailureValidationEngine:
    def __init__(self):
        self.called = False

    def validate(self, context, history):
        self.called = True

        return ValidationExecutionResult(
            success=False,
            attempts=1,
            results=[
                ValidationResult(
                    success=False,
                    validator="ruff",
                    message="Failed",
                )
            ],
        )


class FakeStep:
    def __init__(self):
        self.step = 1
        self.description = "Fake step"


class RetryStepExecutor:
    def __init__(self):
        self.calls = 0

    def execute(self, step, context):
        self.calls += 1

        if self.calls == 1:
            return StepResult(
                step_number=1,
                description="Retry step",
                status=ExecutionStatus.FAILED,
                message="Failed",
                output={},
            )

        return StepResult(
            step_number=1,
            description="Retry step",
            status=ExecutionStatus.SUCCESS,
            message="Success",
            output={},
        )


class RetryFailureAnalyzer:
    def analyze(self, result):
        return SimpleNamespace(
            retryable=True,
            reason="Temporary failure",
            category=SimpleNamespace(value="TRANSIENT"),
        )


class FakeDebugManager:
    def debug(self, result, history, workspace):
        return SimpleNamespace(
            summary="Applied AI fix",
        )


def test_execution_engine_validation_success():
    """
    ExecutionEngine should succeed when
    validation succeeds and persist the executed step.
    """

    validation_engine = SuccessValidationEngine()

    persistence_service = Mock()

    persistence_service.create_execution.return_value = Execution(
        id=1,
        session_id="test-session",
        plan_id=1,
        status="RUNNING",
    )

    engine = ExecutionEngine(
        step_executor=FakeStepExecutor(),
        validation_engine=validation_engine,
        persistence_service=persistence_service,
    )

    context = ExecutionContext(
        workspace=Path("."),
        session_id="test-session",
        plan_id=1,
    )

    context.execution = Execution(
        id=1,
        session_id="test-session",
        plan_id=1,
        status="RUNNING",
    )

    result = engine.execute(
        plan=[FakeStep()],
        context=context,
    )

    assert validation_engine.called is True
    assert result.success is True
    assert len(result.steps) == 1

    persistence_service.record_step.assert_called_once()
    persistence_service.record_validation.assert_called_once()


def test_execution_engine_validation_failure():
    """
    ExecutionEngine should fail when
    validation fails and persist the executed step.
    """

    validation_engine = FailureValidationEngine()

    persistence_service = Mock()

    persistence_service.create_execution.return_value = Execution(
        id=1,
        session_id="test-session",
        plan_id=1,
        status="RUNNING",
    )

    engine = ExecutionEngine(
        step_executor=FakeStepExecutor(),
        validation_engine=validation_engine,
        persistence_service=persistence_service,
    )

    context = ExecutionContext(
        workspace=Path("."),
        session_id="test-session",
        plan_id=1,
    )

    context.execution = Execution(
        id=1,
        session_id="test-session",
        plan_id=1,
        status="RUNNING",
    )

    result = engine.execute(
        plan=[FakeStep()],
        context=context,
    )

    assert validation_engine.called is True
    assert result.success is False
    assert len(result.steps) == 1

    persistence_service.record_step.assert_called_once()
    persistence_service.record_validation.assert_called_once()


def test_execution_engine_records_retry():
    validation_engine = SuccessValidationEngine()

    persistence_service = Mock()

    persistence_service.create_execution.return_value = Execution(
        id=1,
        session_id="test-session",
        plan_id=1,
        status="RUNNING",
    )

    engine = ExecutionEngine(
        step_executor=RetryStepExecutor(),
        validation_engine=validation_engine,
        persistence_service=persistence_service,
        failure_analyzer=RetryFailureAnalyzer(),
    )

    context = ExecutionContext(
        workspace=Path("."),
        session_id="test-session",
        plan_id=1,
    )

    context.execution = Execution(
        id=1,
        session_id="test-session",
        plan_id=1,
        status="RUNNING",
    )

    step = SimpleNamespace(
        step=1,
        description="Retry step",
        action=SimpleNamespace(value="CREATE_FILE"),
    )

    result = engine.execute(
        plan=[step],
        context=context,
    )

    assert result.success is True
    assert persistence_service.record_retry.call_count == 1
    assert persistence_service.record_step.call_count == 2
    assert persistence_service.record_validation.call_count == 1

    persistence_service.record_retry.assert_called_once()


def test_execution_engine_records_debug():
    persistence_service = Mock()

    persistence_service.create_execution.return_value = Execution(
        id=1,
        session_id="test-session",
        plan_id=1,
        status="RUNNING",
    )

    class NoRetryAnalyzer:
        def analyze(self, result):
            return SimpleNamespace(
                retryable=False,
                reason="Syntax error",
                category=SimpleNamespace(value="CODE"),
            )

    class AlwaysFailExecutor:
        def execute(self, step, context):
            return StepResult(
                step_number=1,
                description="Failing step",
                status=ExecutionStatus.FAILED,
                message="Failed",
                output={},
            )

    engine = ExecutionEngine(
        step_executor=AlwaysFailExecutor(),
        validation_engine=SuccessValidationEngine(),
        persistence_service=persistence_service,
        debug_manager=FakeDebugManager(),
        failure_analyzer=NoRetryAnalyzer(),
    )

    context = ExecutionContext(
        workspace=Path("."),
        session_id="test-session",
        plan_id=1,
    )

    context.execution = Execution(
        id=1,
        session_id="test-session",
        plan_id=1,
        status="RUNNING",
    )

    step = SimpleNamespace(
        step=1,
        description="Failing step",
        action=SimpleNamespace(value="CREATE_FILE"),
    )

    engine.execute(
        plan=[step],
        context=context,
    )

    assert (
        persistence_service.record_debug.call_count
        == engine.retry_engine.max_ai_fix_attempts
    )
