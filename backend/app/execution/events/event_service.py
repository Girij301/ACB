from app.execution.context import ExecutionContext
from app.execution.events.event_types import ExecutionEventType
from app.execution.events.execution_event import ExecutionEvent
from app.execution.events.global_publisher import execution_event_publisher
from app.schemas.execution import StepResult
from app.schemas.planner import PlanStep


class EventService:
    """
    High-level service responsible for publishing execution events.

    This keeps ExecutionEngine free from event construction logic.
    """

    def __init__(self) -> None:
        self.publisher = execution_event_publisher

    def execution_started(
        self,
        *,
        context: ExecutionContext,
        total_steps: int,
    ) -> None:
        self.publisher.publish(
            ExecutionEvent(
                type=ExecutionEventType.EXECUTION_STARTED,
                session_id=context.session_id,
                execution_id=(
                    context.execution.id
                    if context.execution is not None
                    else None
                ),
                message="Execution started.",
                payload={
                    "total_steps": total_steps,
                },
            )
        )

    def execution_finished(
        self,
        *,
        context: ExecutionContext,
        success: bool,
    ) -> None:
        self.publisher.publish(
            ExecutionEvent(
                type=ExecutionEventType.EXECUTION_FINISHED,
                session_id=context.session_id,
                execution_id=(
                    context.execution.id
                    if context.execution is not None
                    else None
                ),
                message="Execution completed.",
                payload={
                    "success": success,
                },
            )
        )

    def step_started(
        self,
        *,
        context: ExecutionContext,
        step: PlanStep,
    ) -> None:
        self.publisher.publish(
            ExecutionEvent(
                type=ExecutionEventType.STEP_STARTED,
                session_id=context.session_id,
                execution_id=(
                    context.execution.id
                    if context.execution is not None
                    else None
                ),
                step_number=step.step,
                message=step.description,
                payload={
                    "action": step.action.value,
                    "parameters": step.parameters,
                },
            )
        )

    def step_completed(
        self,
        *,
        context: ExecutionContext,
        step: PlanStep,
        result: StepResult,
    ) -> None:
        self.publisher.publish(
            ExecutionEvent(
                type=ExecutionEventType.STEP_COMPLETED,
                session_id=context.session_id,
                execution_id=(
                    context.execution.id
                    if context.execution is not None
                    else None
                ),
                step_number=step.step,
                message=result.message,
                payload={
                    "status": result.status.value,
                    "output": result.output,
                },
            )
        )

    def retry_started(
        self,
        *,
        context: ExecutionContext,
        step: PlanStep,
        retry_count: int,
        reason: str,
    ) -> None:
        self.publisher.publish(
            ExecutionEvent(
                type=ExecutionEventType.RETRY_STARTED,
                session_id=context.session_id,
                execution_id=(
                    context.execution.id
                    if context.execution is not None
                    else None
                ),
                step_number=step.step,
                message="Retrying step.",
                payload={
                    "retry": retry_count,
                    "reason": reason,
                },
            )
        )

    def debug_started(
        self,
        *,
        context: ExecutionContext,
        step: PlanStep,
        attempt: int,
    ) -> None:
        self.publisher.publish(
            ExecutionEvent(
                type=ExecutionEventType.DEBUG_STARTED,
                session_id=context.session_id,
                execution_id=(
                    context.execution.id
                    if context.execution is not None
                    else None
                ),
                step_number=step.step,
                message="AI debugging started.",
                payload={
                    "attempt": attempt,
                },
            )
        )

    def validation_started(
        self,
        *,
        context: ExecutionContext,
    ) -> None:
        self.publisher.publish(
            ExecutionEvent(
                type=ExecutionEventType.VALIDATION_STARTED,
                session_id=context.session_id,
                execution_id=(
                    context.execution.id
                    if context.execution is not None
                    else None
                ),
                message="Validation started.",
            )
        )

    def validation_completed(
        self,
        *,
        context: ExecutionContext,
        success: bool,
    ) -> None:
        self.publisher.publish(
            ExecutionEvent(
                type=ExecutionEventType.VALIDATION_COMPLETED,
                session_id=context.session_id,
                execution_id=(
                    context.execution.id
                    if context.execution is not None
                    else None
                ),
                message="Validation completed.",
                payload={
                    "success": success,
                },
            )
        )
        
    def retry_completed(
        self,
        *,
        context: ExecutionContext,
        step: PlanStep,
        retry_count: int,
        success: bool,
    ) -> None:
        self.publisher.publish(
            ExecutionEvent(
                type=ExecutionEventType.RETRY_COMPLETED,
                session_id=context.session_id,
                execution_id=(
                    context.execution.id
                    if context.execution is not None
                    else None
                ),
                step_number=step.step,
                message="Retry completed.",
                payload={
                    "retry": retry_count,
                    "success": success,
                },
            )
        )
        
    def debug_completed(
        self,
        *,
        context: ExecutionContext,
        step: PlanStep,
        attempt: int,
        success: bool,
    ) -> None:
        self.publisher.publish(
            ExecutionEvent(
                type=ExecutionEventType.DEBUG_COMPLETED,
                session_id=context.session_id,
                execution_id=(
                    context.execution.id
                    if context.execution is not None
                    else None
                ),
                step_number=step.step,
                message="AI debugging completed.",
                payload={
                    "attempt": attempt,
                    "success": success,
                },
            )
        )