import shutil
from types import SimpleNamespace

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

    def debug(self, result, history, workspace):
        return (
            SimpleNamespace(
                retryable=False,
                reason="Test failure",
                category=SimpleNamespace(value="TEST"),
            ),
            SimpleNamespace(
                patches=[],
            ),
        )


def test_workspace_sync():
    """
    Verify that files created on the host workspace
    are immediately visible inside the Docker container.
    """

    # ------------------------------------------------------------------
    # Ensure a clean test workspace before running the test
    # ------------------------------------------------------------------
    test_workspace = WORKSPACE_DIR / "workspace_sync_test"

    if test_workspace.exists():
        shutil.rmtree(test_workspace, ignore_errors=True)

    test_workspace.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Test plan
    # ------------------------------------------------------------------
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

    # ------------------------------------------------------------------
    # Execution context
    # ------------------------------------------------------------------
    context = ExecutionContext(
        session_id="workspace-test",
        plan_id="workspace-test",
        workspace=test_workspace,
    )

    # ------------------------------------------------------------------
    # Execute
    # ------------------------------------------------------------------
    engine = ExecutionEngine(
        debug_manager=FakeDebugManager(),
    )

    result = engine.execute(plan, context)

    # ------------------------------------------------------------------
    # Debug output
    # ------------------------------------------------------------------
    print("\n--- STEP RESULTS ---")

    for step_result in result.steps:
        print(f"\nSTEP {step_result.step_number}")
        print("STATUS:", step_result.status)
        print("OUTPUT:", step_result.output)

    # ------------------------------------------------------------------
    # Assertions
    # ------------------------------------------------------------------
    assert result.success

    assert result.steps[2].status.value == "success"

    assert "Hello Docker" in result.steps[2].output["stdout"]
