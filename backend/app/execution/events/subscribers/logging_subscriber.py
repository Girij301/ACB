from app.core.logger import logger
from app.execution.events.execution_event import ExecutionEvent
from app.execution.events.execution_event_subscriber import ExecutionEventSubscriber


class LoggingSubscriber(ExecutionEventSubscriber):
    """
    Subscriber that logs execution events for observability.
    """

    def handle(
        self,
        event: ExecutionEvent,
    ) -> None:
        logger.info(
            "[%s] session=%s execution=%s step=%s message=%s payload=%s",
            event.type.value,
            event.session_id,
            event.execution_id,
            event.step_number,
            event.message,
            event.payload,
        )
