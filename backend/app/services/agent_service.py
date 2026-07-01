from app.core.config import settings
from app.execution.context import ExecutionContext
from app.schemas.execute import ExecuteRequest
from app.schemas.execution import ExecutionResult
from app.services.execution_service import ExecutionService
from app.services.planner_service import PlannerService


class AgentService:
    """
    High-level orchestration service for the AI agent.

    Flow:
        User Task
            ↓
        PlannerService
            ↓
        ExecutionService
            ↓
        ExecutionResult
    """

    def __init__(
        self,
        planner_service: PlannerService | None = None,
        execution_service: ExecutionService | None = None,
    ) -> None:
        self.planner_service = (
            planner_service or PlannerService()
        )

        self.execution_service = (
            execution_service or ExecutionService()
        )

    def execute(
        self,
        request: ExecuteRequest,
    ) -> ExecutionResult:
        """
        Generate a plan and execute it.
        """

        planner_response = self.planner_service.create_plan(
            request.task,
        )

        return self.execution_service.execute_plan(
            plan=planner_response.plan,
            workspace=settings.WORKSPACE_DIR,
            plan_id=1,
        )