from app.core.logger import logger
from app.debugger.debug_manager import DebugManager
from app.execution.context import ExecutionContext
from app.execution.failure_analyzer import FailureAnalyzer
from app.execution.retry_engine import RetryEngine
from app.execution.step_executor import StepExecutor
from app.execution.validation_engine import ValidationEngine
from app.schemas.execution import ExecutionResult, ExecutionStatus
from app.schemas.execution_memory import ExecutionMemory
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
    ) -> None:
        self.step_executor = step_executor or StepExecutor()
        self.retry_engine = retry_engine or RetryEngine()
        self.failure_analyzer = failure_analyzer or FailureAnalyzer()
        self.debug_manager = debug_manager or DebugManager()
        self.validation_engine = validation_engine or ValidationEngine()
        self.persistence_service = persistence_service

    def execute(
        self,
        plan: list,
        context: ExecutionContext,
    ) -> ExecutionResult:
        """
        Execute all plan steps sequentially with
        automatic retries and AI-powered debugging.
        """

        memory = ExecutionMemory()

        if self.persistence_service is not None:
            context.execution = self.persistence_service.create_execution(
                session_id=context.session_id,
                plan_id=context.plan_id,
            )

        for step in plan:

            memory.reset_retry()
            memory.reset_ai_fix_attempts()

            while True:

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

                    continue

                logger.error(
                    f"Step {step.step} failed after " f"{memory.retry_count} retries."
                )

                memory.increment_ai_fix_attempt()

                if memory.ai_fix_attempts > self.retry_engine.max_ai_fix_attempts:
                    logger.error("Maximum AI fix attempts reached.")

                    return ExecutionResult(
                        success=False,
                        steps=memory.step_results,
                    )

                logger.info("Requesting AI debugging...")

                debug_result = self.debug_manager.debug(
                    result=result,
                    history=[
                        step_result.model_dump() for step_result in memory.step_results
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

                logger.info("Retrying step after AI patch...")

                memory.reset_retry()

                continue

        validation = self.validation_engine.validate(
            context=context,
            history=[step_result.model_dump() for step_result in memory.step_results],
        )

        if self.persistence_service is not None and context.execution is not None:
            for validation_result in validation.results:
                self.persistence_service.record_validation(
                    execution=context.execution,
                    validation_result=validation_result,
                )

        if not validation.success:

            logger.error("Workspace validation failed.")

            return ExecutionResult(
                success=False,
                steps=memory.step_results,
            )

        logger.info("Workspace validation passed.")

        return ExecutionResult(
            success=True,
            steps=memory.step_results,
        )
