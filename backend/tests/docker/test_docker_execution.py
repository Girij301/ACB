from pathlib import Path

from app.core.config import settings
from app.execution.context import ExecutionContext
from app.execution.engine import ExecutionEngine
from app.schemas.planner import ActionType, PlanStep


def test_python_version_inside_docker():
    workspace = settings.WORKSPACE_DIR / "docker_version_test"
    workspace.mkdir(parents=True, exist_ok=True)

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
        workspace=workspace,
    )

    engine = ExecutionEngine()

    result = engine.execute(
        plan=plan,
        context=context,
    )

    assert result.success
    assert result.steps[0].status.value == "SUCCESS"
    assert "Python" in result.steps[0].output["stdout"]