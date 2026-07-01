from pathlib import Path

from app.core.logger import logger
from app.debugger.debug_agent import DebugAgent
from app.debugger.patch_applier import PatchApplier
from app.execution.failure_analyzer import FailureAnalyzer
from app.schemas.execution import StepResult
from app.schemas.validation import ValidationResult


class DebugManager:
    """
    Coordinates the complete debugging workflow.
    """

    def __init__(
        self,
        failure_analyzer: FailureAnalyzer | None = None,
        debug_agent: DebugAgent | None = None,
        patch_applier: PatchApplier | None = None,
    ) -> None:
        self.failure_analyzer = failure_analyzer or FailureAnalyzer()
        self.debug_agent = debug_agent or DebugAgent()
        self.patch_applier = patch_applier or PatchApplier()

    def debug(
        self,
        result: StepResult | ValidationResult,
        history: list,
        workspace: Path,
    ):
        """
        Analyze a failure, ask Gemini for a fix,
        and apply the generated patch.
        """

        analysis = self.failure_analyzer.analyze(result)

        logger.info(
            "Failure Analysis | "
            f"Category={analysis.category.value} | "
            f"Retryable={analysis.retryable} | "
            f"Reason={analysis.reason}"
        )

        if isinstance(result, StepResult):
            failure = result.output or {}
        else:
            failure = result.model_dump()

        suggestion = self.debug_agent.analyze(
            failure=failure,
            history=history,
        )

        logger.info("Debug Suggestion | " f"Summary={suggestion.summary}")

        self.patch_applier.apply(
            suggestion=suggestion,
            workspace=workspace,
        )

        return analysis, suggestion
