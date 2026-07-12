from app.core.logger import logger
from app.execution.events.execution_event import ExecutionEvent
from app.execution.events.execution_event_subscriber import ExecutionEventSubscriber


class ExecutionEventPublisher:
    """
    Simple in-memory publisher for execution events.
    """

    def __init__(self) -> None:
        self._subscribers: list[ExecutionEventSubscriber] = []

    def subscribe(
        self,
        subscriber: ExecutionEventSubscriber,
    ) -> None:
        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)

    def unsubscribe(
        self,
        subscriber: ExecutionEventSubscriber,
    ) -> None:
        if subscriber in self._subscribers:
            self._subscribers.remove(subscriber)

    def publish(self, event: ExecutionEvent) -> None:
        logger.info(
            "Publishing %s",
            event.type,
        )

        for subscriber in self._subscribers:
            try:
                subscriber.handle(event)
            except Exception:
                logger.exception(
                    "Subscriber %s failed",
                    type(subscriber).__name__,
                )
