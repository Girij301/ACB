from unittest.mock import Mock

from app.execution.events.event_service import EventService
from app.execution.events.event_types import ExecutionEventType
from app.schemas.execution import ExecutionStatus, StepResult
from app.schemas.planner import ActionType


def test_execution_started_event():
    service = EventService()

    service.publisher = Mock()

    context = Mock()
    context.session_id = "test-session"
    context.plan_id = 1
    context.workspace = "/workspace"
    context.execution = None

    service.execution_started(
        context=context,
        total_steps=3,
    )

    service.publisher.publish.assert_called_once()

    event = service.publisher.publish.call_args.args[0]

    assert event.type == ExecutionEventType.EXECUTION_STARTED
    assert event.session_id == "test-session"
    assert event.payload["total_steps"] == 3
    assert event.payload["plan_id"] == 1


def test_step_completed_event():
    service = EventService()

    service.publisher = Mock()

    context = Mock()
    context.session_id = "test-session"
    context.execution = None

    step = Mock()
    step.step = 1
    step.action = ActionType.CREATE_FILE
    step.parameters = {}

    result = StepResult(
        step_number=1,
        description="Create file",
        status=ExecutionStatus.SUCCESS,
        message="Success",
        output={},
    )

    service.step_completed(
        context=context,
        step=step,
        result=result,
    )

    event = service.publisher.publish.call_args.args[0]

    assert event.type == ExecutionEventType.STEP_COMPLETED
    assert event.step_number == 1
    assert event.payload["status"] == "success"
