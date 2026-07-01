from pathlib import Path

from app.execution.context import ExecutionContext
from app.execution.engine import ExecutionEngine
from app.schemas.execution import ExecutionResult


class ExecutionService:
    """
    Service responsible for coordinating plan execution.

    It prepares the execution context and delegates the
    execution workflow to the ExecutionEngine.
    """

    def __init__(
        self,
        engine: ExecutionEngine | None = None,
    ) -> None:
        self.engine = engine or ExecutionEngine()

    def execute_plan(
        self,
        *,
        plan: list[dict],
        workspace: Path,
        plan_id: int,
    ) -> ExecutionResult:
        """
        Execute an entire plan.

        Args:
            plan: Planner output.
            workspace: Workspace directory.
            plan_id: Database identifier for the plan.

        Returns:
            ExecutionResult
        """

        context = ExecutionContext(
            workspace=workspace,
            plan_id=plan_id,
        )

        return self.engine.execute(
            plan=plan,
            context=context,
        )
