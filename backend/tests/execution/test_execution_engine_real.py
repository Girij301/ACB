from pathlib import Path

from app.execution.context import ExecutionContext
from app.execution.engine import ExecutionEngine
from app.schemas.planner import ActionType, PlanStep
from app.schemas.validation import ValidationResult
from app.schemas.validation_execution import ValidationExecutionResult


class FakeValidationEngine:
    def validate(self, context, history):
        return ValidationExecutionResult(
            success=True,
            attempts=1,
            results=[
                ValidationResult(
                    success=True,
                    validator="fake",
                    message="Passed",
                )
            ],
        )


def test_execution_engine_creates_real_file(tmp_path: Path):
    """
    ExecutionEngine should execute a real CREATE_FILE
    step successfully.
    """

    engine = ExecutionEngine(
        validation_engine=FakeValidationEngine(),
    )

    context = ExecutionContext(
        workspace=tmp_path,
        session_id="test-session",
        plan_id=1,
    )

    plan = [
        PlanStep(
            step=1,
            action=ActionType.CREATE_FILE,
            description="Create hello.txt",
            parameters={
                "relative_path": "hello.txt",
                "content": "Hello from ExecutionEngine",
            },
        )
    ]

    result = engine.execute(
        plan=plan,
        context=context,
    )

    assert result.success is True

    created_file = tmp_path / "hello.txt"

    assert created_file.exists()
    assert created_file.read_text() == "Hello from ExecutionEngine"
