import asyncio

from app.core import event_loop as loop_holder
from app.core.logger import logger
from app.execution.events.execution_event import ExecutionEvent
from app.execution.events.execution_event_subscriber import (
    ExecutionEventSubscriber,
)
from app.websocket.connection_manager import connection_manager


class WebSocketSubscriber(ExecutionEventSubscriber):

    def handle(self, event: ExecutionEvent) -> None:

        if loop_holder.event_loop is None:
            logger.error("WebSocket event loop is not initialized.")
            return

        future = asyncio.run_coroutine_threadsafe(
            connection_manager.send(
                session_id=event.session_id,
                message=event.model_dump(mode="json"),
            ),
            loop_holder.event_loop,
        )

        try:
            future.result(timeout=5)
        except Exception:
            logger.exception(
                "Failed to send execution event via WebSocket."
            )