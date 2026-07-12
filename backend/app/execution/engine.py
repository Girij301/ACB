from app.core.logger import logger
from app.debugger.debug_manager import DebugManager
from app.docker.docker_manager import DockerManager
from app.docker.execution_container import ExecutionContainer
from app.docker.sandbox import DEFAULT_SANDBOX
from app.execution.context import ExecutionContext
from app.execution.events.event_service import EventService
from app.execution.failure_analyzer import FailureAnalyzer
from app.execution.retry_engine import RetryEngine
from app.execution.step_executor import StepExecutor
from app.execution.validation_engine import ValidationEngine
from app.schemas.execution import ExecutionResult, ExecutionStatus
from app.schemas.execution_memory import ExecutionMemory
from app.schemas.planner import PlanStep
from app.services.execution_persistence_service import ExecutionPersistenceService


class ExecutionEngine:
    """
    Coordinates execution of an entire plan.
    """

    def __init__(
        self,
        step_executor: StepExecutor | None = None,
        retry_engine: RetryEngine | None = None,
        failure_analyzer: FailureAnalyzer | None = None,
        debug_manager: DebugManager | None = None,
        validation_engine: ValidationEngine | None = None,
        persistence_service: ExecutionPersistenceService | None = None,
        event_service: EventService | None = None,
    ) -> None:
        self.step_executor = step_executor or StepExecutor()
        self.retry_engine = retry_engine or RetryEngine()
        self.failure_analyzer = failure_analyzer or FailureAnalyzer()
        self.debug_manager = debug_manager or DebugManager()
        self.validation_engine = validation_engine or ValidationEngine()
        self.persistence_service = persistence_service
        self.events = event_service or EventService()

    def _build_result(
        self,
        *,
        success: bool,
        memory: ExecutionMemory,
        context: ExecutionContext,
    ) -> ExecutionResult:
        execution_summary = None

        if self.persistence_service is not None and context.execution is not None:
            execution_summary = self.persistence_service.build_execution_summary(
                execution=context.execution,
                workspace=str(context.workspace),
            )

        return ExecutionResult(
            success=success,
            steps=memory.step_results,
            execution=execution_summary,
        )

    def execute(
        self,
        plan: list[PlanStep],
        context: ExecutionContext,
    ) -> ExecutionResult:
        """
        Execute all plan steps sequentially with
        automatic retries and AI-powered debugging.
        """

        memory = ExecutionMemory()

        finished_event_sent = False

        container = ExecutionContainer(
            DockerManager(),
            DEFAULT_SANDBOX.to_container_config(),
        )

        container.create()
        container.start()

        context.container = container

        try:

            if self.persistence_service is not None:
                context.execution = self.persistence_service.create_execution(
                    session_id=context.session_id,
                    plan_id=context.plan_id,
                    total_steps=len(plan),
                )
            self.events.execution_started(
                context=context,
                total_steps=len(plan),
            )

            for step in plan:

                memory.reset_retry()
                memory.reset_ai_fix_attempts()

                while True:

                    self.events.step_started(
                        context=context,
                        step=step,
                    )

                    result = self.step_executor.execute(
                        step=step,
                        context=context,
                    )

                    memory.add_result(result)

                    if (
                        self.persistence_service is not None
                        and context.execution is not None
                    ):
                        self.persistence_service.record_step(
                            execution=context.execution,
                            step=step,
                            result=result,
                        )

                    self.events.step_completed(
                        context=context,
                        step=step,
                        result=result,
                    )

                    if result.status == ExecutionStatus.SUCCESS:
                        break

                    analysis = self.failure_analyzer.analyze(result)

                    logger.info(
                        "Failure Analysis | "
                        f"Category={analysis.category.value} | "
                        f"Retryable={analysis.retryable} | "
                        f"Reason={analysis.reason}"
                    )

                    memory.increment_retry()

                    should_retry = self.retry_engine.should_retry(
                        analysis,
                        memory.retry_count,
                    )

                    if should_retry:

                        if (
                            self.persistence_service is not None
                            and context.execution is not None
                        ):
                            self.persistence_service.record_retry(
                                execution=context.execution,
                                step=step,
                                retry_attempt=memory.retry_count,
                                analysis=analysis,
                                previous_error=getattr(result, "error", None),
                                success=False,
                            )

                        logger.info(
                            f"Retrying step {step.step} "
                            f"(attempt "
                            f"{memory.retry_count}/"
                            f"{self.retry_engine.max_retries})"
                        )

                        self.events.retry_started(
                            context=context,
                            step=step,
                            retry_count=memory.retry_count,
                            reason=analysis.reason,
                        )

                        self.events.retry_completed(
                            context=context,
                            step=step,
                            retry_count=memory.retry_count,
                            success=False,
                        )

                        continue

                    logger.error(
                        f"Step {step.step} failed after "
                        f"{memory.retry_count} retries."
                    )

                    memory.increment_ai_fix_attempt()

                    if memory.ai_fix_attempts > self.retry_engine.max_ai_fix_attempts:

                        logger.error("Maximum AI fix attempts reached.")

                        if (
                            self.persistence_service is not None
                            and context.execution is not None
                        ):
                            self.persistence_service.complete_execution(
                                execution=context.execution,
                                success=False,
                            )
                        self.events.execution_finished(
                            context=context,
                            success=False,
                        )
                        finished_event_sent = True
                        return self._build_result(
                            success=False,
                            memory=memory,
                            context=context,
                        )

                    logger.info("Requesting AI debugging...")

                    self.events.debug_started(
                        context=context,
                        step=step,
                        attempt=memory.ai_fix_attempts,
                    )

                    debug_result = self.debug_manager.debug(
                        result=result,
                        history=[
                            step_result.model_dump()
                            for step_result in memory.step_results
                        ],
                        workspace=context.workspace,
                    )

                    if (
                        self.persistence_service is not None
                        and context.execution is not None
                    ):
                        self.persistence_service.record_debug(
                            execution=context.execution,
                            step=step,
                            attempt_number=memory.ai_fix_attempts,
                            failure_summary=analysis.reason,
                            ai_summary=(
                                getattr(debug_result, "summary", None)
                                if debug_result is not None
                                else None
                            ),
                            success=debug_result is not None,
                        )

                    self.events.debug_completed(
                        context=context,
                        step=step,
                        attempt=memory.ai_fix_attempts,
                        success=debug_result is not None,
                    )

                    logger.info("Retrying step after AI patch...")

                    memory.reset_retry()

            self.events.validation_started(
                context=context,
            )

            validation = self.validation_engine.validate(
                context=context,
                history=[
                    step_result.model_dump() for step_result in memory.step_results
                ],
            )

            if self.persistence_service is not None and context.execution is not None:
                for validation_result in validation.results:
                    self.persistence_service.record_validation(
                        execution=context.execution,
                        validation_result=validation_result,
                    )

            self.events.validation_completed(
                context=context,
                success=validation.success,
            )

            if not validation.success:

                logger.error("Workspace validation failed.")

                if (
                    self.persistence_service is not None
                    and context.execution is not None
                ):
                    self.persistence_service.complete_execution(
                        execution=context.execution,
                        success=False,
                    )

                self.events.execution_finished(
                    context=context,
                    success=False,
                )
                finished_event_sent = True

                return self._build_result(
                    success=False,
                    memory=memory,
                    context=context,
                )

            logger.info("Workspace validation passed.")

            if self.persistence_service is not None and context.execution is not None:
                self.persistence_service.complete_execution(
                    execution=context.execution,
                    success=True,
                )
            self.events.execution_finished(
                context=context,
                success=True,
            )
            finished_event_sent = True
            return self._build_result(
                success=True,
                memory=memory,
                context=context,
            )

        except Exception:

            if not finished_event_sent:
                self.events.execution_finished(
                    context=context,
                    success=False,
                )

            raise

        finally:
            if context.container is not None:
                context.container.close()
                context.container = None
