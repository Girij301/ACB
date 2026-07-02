from pathlib import Path

from app.execution.context import ExecutionContext
from app.execution.step_executor import StepExecutor
from app.schemas.execution import ExecutionStatus
from app.schemas.planner import ActionType, PlanStep


def test_create_file(tmp_path: Path):
    """
    StepExecutor should create a file
    using the real FileTool.
    """

    context = ExecutionContext(
        workspace=tmp_path,
        session_id="test-session",
        plan_id=1,
    )

    executor = StepExecutor()

    step = PlanStep(
        step=1,
        action=ActionType.CREATE_FILE,
        description="Create hello.txt",
        parameters={
            "relative_path": "hello.txt",
            "content": "Hello World",
        },
    )

    result = executor.execute(
        step=step,
        context=context,
    )

    assert result.status == ExecutionStatus.SUCCESS

    created_file = tmp_path / "hello.txt"

    assert created_file.exists()
    assert created_file.read_text() == "Hello World"
