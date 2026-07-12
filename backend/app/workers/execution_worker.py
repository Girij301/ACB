from threading import Thread

from app.core.database import SessionLocal
from app.core.logger import logger
from app.schemas.execute import ExecuteRequest
from app.services.agent_service import AgentService


class ExecutionWorker:
    """
    Runs a complete agent execution in a background thread.

    Each worker owns its own database session so it is completely
    independent of the FastAPI request lifecycle.
    """

    @staticmethod
    def _run(request: ExecuteRequest) -> None:
        db = SessionLocal()

        try:
            logger.info(
                "Background execution started | session=%s",
                request.session_id,
            )

            agent = AgentService(db=db)

            agent.execute(request)

            logger.info(
                "Background execution finished | session=%s",
                request.session_id,
            )

        except Exception:
            logger.exception(
                "Background execution failed | session=%s",
                request.session_id,
            )

        finally:
            db.close()

    @classmethod
    def start(
        cls,
        request: ExecuteRequest,
    ) -> Thread:
        """
        Spawn a daemon thread for execution.

        Returns
        -------
        Thread
            The running background thread.
        """

        thread = Thread(
            target=cls._run,
            args=(request,),
            daemon=True,
            name=f"execution-{request.session_id}",
        )

        thread.start()

        return thread
