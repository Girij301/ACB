from app.core.logger import logger
from app.debugger.debug_manager import DebugManager
from app.execution.context import ExecutionContext
from app.execution.failure_analyzer import FailureAnalyzer
from app.execution.retry_engine import RetryEngine
from app.execution.step_executor import StepExecutor
from app.execution.validation_engine import ValidationEngine
from app.schemas.execution import ExecutionResult, ExecutionStatus
from app.schemas.execution_memory import ExecutionMemory


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
    ) -> None:
        self.step_executor = step_executor or StepExecutor()
        self.retry_engine = retry_engine or RetryEngine()
        self.failure_analyzer = failure_analyzer or FailureAnalyzer()
        self.debug_manager = debug_manager or DebugManager()
        self.validation_engine = validation_engine or ValidationEngine()

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

        for step in plan:

            memory.reset_retry()
            memory.reset_ai_fix_attempts()

            while True:

                result = self.step_executor.execute(
                    step=step,
                    context=context,
                )

                memory.add_result(result)

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

                memory.increment_ai_fix_attempts()

                if memory.ai_fix_attempts > self.retry_engine.max_ai_fix_attempts:
                    logger.error("Maximum AI fix attempts reached.")

                    return ExecutionResult(
                        success=False,
                        steps=memory.step_results,
                    )

                logger.info("Requesting AI debugging...")

                self.debug_manager.debug(
                    result=result,
                    history=[
                        step_result.model_dump() for step_result in memory.step_results
                    ],
                    workspace=context.workspace,
                )

                logger.info("Retrying step after AI patch...")

                memory.reset_retry()

                continue

        validation = self.validation_engine.validate(
            context=context,
            history=[step_result.model_dump() for step_result in memory.step_results],
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
