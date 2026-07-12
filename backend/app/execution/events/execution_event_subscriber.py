from abc import ABC, abstractmethod

from app.execution.events.execution_event import ExecutionEvent


class ExecutionEventSubscriber(ABC):
    """
    Base class for all execution event subscribers.
    """

    @abstractmethod
    def handle(
        self,
        event: ExecutionEvent,
    ) -> None:
        """
        Handle an execution event.
        """
        raise NotImplementedError
