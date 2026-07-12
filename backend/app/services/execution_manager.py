from threading import Lock, Thread

from app.core.logger import logger
from app.schemas.execute import ExecuteRequest
from app.workers.execution_worker import ExecutionWorker


class ExecutionManager:
    """
    Manages background execution workers.

    Responsibilities
    ----------------
    - Start new executions
    - Prevent duplicate executions for the same session
    - Track currently running threads
    - Clean up completed threads

    This class will later become the integration point for:
        - SSE
        - WebSockets
        - Execution cancellation
        - Queueing
    """

    def __init__(self) -> None:
        self._threads: dict[str, Thread] = {}
        self._lock = Lock()

    def start(
        self,
        request: ExecuteRequest,
    ) -> bool:
        """
        Start a background execution.

        Returns
        -------
        bool
            True if execution was started.
            False if one is already running.
        """

        with self._lock:
            self._cleanup()

            existing = self._threads.get(request.session_id)

            if existing and existing.is_alive():
                logger.warning(
                    "Execution already running | session=%s",
                    request.session_id,
                )
                return False

            thread = ExecutionWorker.start(request)

            self._threads[request.session_id] = thread

            logger.info(
                "Execution registered | session=%s",
                request.session_id,
            )

            return True

    def is_running(
        self,
        session_id: str,
    ) -> bool:
        """
        Check whether a session currently has an active execution.
        """

        with self._lock:
            thread = self._threads.get(session_id)

            if thread is None:
                return False

            return thread.is_alive()

    def _cleanup(self) -> None:
        """
        Remove completed threads.
        """

        completed = [
            session_id
            for session_id, thread in self._threads.items()
            if not thread.is_alive()
        ]

        for session_id in completed:
            self._threads.pop(session_id, None)


execution_manager = ExecutionManager()