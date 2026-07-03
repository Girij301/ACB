from pathlib import Path

from app.execution.context import ExecutionContext
from app.execution.step_executor import StepExecutor
from app.schemas.execution import ExecutionStatus
from app.schemas.planner import ActionType, PlanStep


def test_run_terminal_command():
    """
    StepExecutor should execute a terminal command.
    """

    context = ExecutionContext(
        workspace=Path("."),
        session_id="test-session",
        plan_id=1,
    )

    executor = StepExecutor()

    step = PlanStep(
        step=1,
        action=ActionType.RUN_TERMINAL,
        description="Run Python version",
        parameters={
            "command": "python --version",
            "cwd": ".",
        },
    )

    result = executor.execute(
        step=step,
        context=context,
    )

    print("STATUS:", result.status)
    print("MESSAGE:", result.message)
    print("OUTPUT:", result.output)
    assert result.status == ExecutionStatus.SUCCESS
    assert result.output["exit_code"] == 0
    assert "Python" in result.output["stdout"]
