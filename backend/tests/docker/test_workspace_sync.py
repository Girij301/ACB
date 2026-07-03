
from app.core.config import WORKSPACE_DIR
from app.execution.context import ExecutionContext
from app.execution.engine import ExecutionEngine
from app.schemas.planner import ActionType, PlanStep


def test_workspace_sync():
    plan = [
        PlanStep(
            step=1,
            action=ActionType.CREATE_FILE,
            description="Create hello.txt",
            parameters={
                "relative_path": "hello.txt",
            },
        ),
        PlanStep(
            step=2,
            action=ActionType.WRITE_FILE,
            description="Write file",
            parameters={
                "relative_path": "hello.txt",
                "content": "Hello Docker",
            },
        ),
        PlanStep(
            step=3,
            action=ActionType.RUN_TERMINAL,
            description="Read file inside Docker",
            parameters={
                "command": "cat hello.txt",
            },
        ),
    ]

    context = ExecutionContext(
        session_id="workspace-test",
        plan_id="workspace-test",
        workspace=WORKSPACE_DIR,
    )

    engine = ExecutionEngine()

    result = engine.execute(plan, context)

    assert result.success
    assert result.steps[2].status.value == "success"
    assert "Hello Docker" in result.steps[2].output["stdout"]
