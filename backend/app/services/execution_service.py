from pathlib import Path

from sqlalchemy.orm import Session

from app.execution.context import ExecutionContext
from app.execution.engine import ExecutionEngine
from app.repositories.debug_repository import DebugRepository
from app.repositories.execution_repository import ExecutionRepository
from app.repositories.execution_step_repository import (
    ExecutionStepRepository,
)
from app.repositories.retry_repository import RetryRepository
from app.repositories.validation_repository import (
    ValidationRepository,
)
from app.schemas.execution import ExecutionResult
from app.schemas.planner import PlanStep
from app.services.execution_persistence_service import (
    ExecutionPersistenceService,
)


class ExecutionService:
    """
    Service responsible for coordinating plan execution.

    It prepares the execution context and delegates the
    execution workflow to the ExecutionEngine.
    """

    def __init__(
        self,
        db: Session,
        engine: ExecutionEngine | None = None,
    ) -> None:

        persistence_service = ExecutionPersistenceService(
            execution_repository=ExecutionRepository(db),
            execution_step_repository=ExecutionStepRepository(db),
            validation_repository=ValidationRepository(db),
            retry_repository=RetryRepository(db),
            debug_repository=DebugRepository(db),
        )

        if engine is None:
            self.engine = ExecutionEngine(
                persistence_service=persistence_service,
            )
        else:
            self.engine = engine
            self.engine.persistence_service = persistence_service

    def execute_plan(
        self,
        *,
        plan: list[PlanStep],
        workspace: Path,
        session_id: str,
        plan_id: int,
    ) -> ExecutionResult:
        """
        Execute an entire plan.

        Args:
            plan: Planner output.
            workspace: Workspace directory.
            session_id: Current execution session.
            plan_id: Database identifier for the plan.

        Returns:
            ExecutionResult
        """

        context = ExecutionContext(
            workspace=workspace,
            session_id=session_id,
            plan_id=plan_id,
        )

        return self.engine.execute(
            plan=plan,
            context=context,
        )