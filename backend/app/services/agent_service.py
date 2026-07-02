from app.core.config import settings
from app.schemas.execute import ExecuteRequest
from app.schemas.execution import ExecutionResult
from app.services.execution_service import ExecutionService
from app.services.planner_service import PlannerService
from sqlalchemy.orm import Session


class AgentService:
    """
    High-level orchestration service for the AI agent.

    Flow:

        User Request
             │
             ▼
      PlannerService
             │
             ▼
     ExecutionService
             │
             ▼
      ExecutionEngine
             │
             ▼
    ExecutionPersistenceService
             │
             ▼
        Repository Layer
    """

    def __init__(
        self,
        db: Session,
        planner_service: PlannerService | None = None,
        execution_service: ExecutionService | None = None,
    ) -> None:

        self.planner_service = planner_service or PlannerService()

        self.execution_service = execution_service or ExecutionService(db=db)

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
            session_id=request.session_id,
            plan_id=1,
        )
