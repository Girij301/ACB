from pathlib import Path

from app.execution.context import ExecutionContext
from app.execution.engine import ExecutionEngine
from app.schemas.planner import ActionType, PlanStep


def test_python_version_inside_docker():
    plan = [
        PlanStep(
            step=1,
            action=ActionType.RUN_TERMINAL,
            description="Check Python version",
            parameters={
                "command": "python --version",
            },
        )
    ]

    context = ExecutionContext(
        session_id="test-session",
        plan_id="test-plan",
        workspace=Path("workspace"),
    )

    engine = ExecutionEngine()

    result = engine.execute(
        plan=plan,
        context=context,
    )

    assert result.success
    assert result.steps[0].status.value == "success"
    assert "Python" in result.steps[0].output["stdout"]
