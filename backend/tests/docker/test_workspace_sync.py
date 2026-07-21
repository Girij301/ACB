import shutil

from app.core.config import WORKSPACE_DIR
from app.execution.context import ExecutionContext
from app.execution.engine import ExecutionEngine
from app.schemas.planner import ActionType, PlanStep


class FakePatchApplier:
    def apply_command_patches(self, suggestion, step):
        return step


class FakeDebugManager:
    def __init__(self):
        self.patch_applier = FakePatchApplier()

    def debug(self, result, history, workspace, step=None):
        return (
            type(
                "FailureAnalysis",
                (),
                {
                    "retryable": False,
                    "reason": "Test failure",
                    "category": type(
                        "Category",
                        (),
                        {"value": "TEST"},
                    ),
                },
            )(),
            type(
                "DebugSuggestion",
                (),
                {
                    "summary": "No patch required",
                    "patches": [],
                },
            )(),
            step,
        )


def test_workspace_sync():
    """
    Verify that files created and modified on the host workspace
    are immediately visible inside the Docker container.
    """

    # ---------------------------------------------------------
    # Prepare clean workspace
    # ---------------------------------------------------------

    test_workspace = WORKSPACE_DIR / "workspace_sync_test"

    if test_workspace.exists():
        shutil.rmtree(test_workspace, ignore_errors=True)

    test_workspace.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------
    # Execution plan
    # ---------------------------------------------------------

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
            description="Write content to hello.txt",
            parameters={
                "relative_path": "hello.txt",
                "content": "Hello Docker",
            },
        ),
        PlanStep(
            step=3,
            action=ActionType.RUN_TERMINAL,
            description="Read hello.txt inside Docker",
            parameters={
                "command": "cat hello.txt",
            },
        ),
    ]

    # ---------------------------------------------------------
    # Execution context
    # ---------------------------------------------------------

    context = ExecutionContext(
        session_id="workspace-test",
        plan_id="workspace-test",
        workspace=test_workspace,
    )

    # ---------------------------------------------------------
    # Execute plan
    # ---------------------------------------------------------

    engine = ExecutionEngine(
        debug_manager=FakeDebugManager(),
    )

    result = engine.execute(
        plan=plan,
        context=context,
    )

    # ---------------------------------------------------------
    # Host filesystem verification
    # ---------------------------------------------------------

    test_file = test_workspace / "hello.txt"

    assert test_file.exists(), (
        "hello.txt should exist on the host workspace"
    )

    host_content = test_file.read_text(
        encoding="utf-8",
    )

    assert host_content == "Hello Docker"

    # ---------------------------------------------------------
    # Execution verification
    # ---------------------------------------------------------

    assert result.success, (
        f"Execution failed: {result.steps}"
    )

    assert len(result.steps) == 3

    assert result.steps[0].status.value == "SUCCESS"

    assert result.steps[1].status.value == "SUCCESS"

    assert result.steps[2].status.value == "SUCCESS"

    assert (
        "Hello Docker"
        in result.steps[2].output["stdout"]
    )