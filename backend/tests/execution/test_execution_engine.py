from pathlib import Path

from app.execution.context import ExecutionContext
from app.execution.engine import ExecutionEngine
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


def test_execution_engine_validation_success():
    """
    ExecutionEngine should succeed when
    validation succeeds.
    """

    validation_engine = SuccessValidationEngine()

    engine = ExecutionEngine(
        step_executor=FakeStepExecutor(),
        validation_engine=validation_engine,
    )

    context = ExecutionContext(
        workspace=Path("."),
        plan_id=1,
    )

    result = engine.execute(
        plan=[FakeStep()],
        context=context,
    )

    assert validation_engine.called is True
    assert result.success is True
    assert len(result.steps) == 1


def test_execution_engine_validation_failure():
    """
    ExecutionEngine should fail when
    validation fails.
    """

    validation_engine = FailureValidationEngine()

    engine = ExecutionEngine(
        step_executor=FakeStepExecutor(),
        validation_engine=validation_engine,
    )

    context = ExecutionContext(
        workspace=Path("."),
        plan_id=1,
    )

    result = engine.execute(
        plan=[FakeStep()],
        context=context,
    )

    assert validation_engine.called is True
    assert result.success is False
    assert len(result.steps) == 1
