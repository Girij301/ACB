from pathlib import Path

from app.core.logger import logger
from app.debugger.debug_agent import DebugAgent
from app.debugger.patch_applier import PatchApplier
from app.execution.failure_analyzer import FailureAnalyzer
from app.schemas.debug import DebugSuggestion
from app.schemas.execution import StepResult
from app.schemas.failure import FailureAnalysis
from app.schemas.planner import PlanStep
from app.schemas.validation import ValidationResult
from app.tools.file_tool import FileTool

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
        step: PlanStep | None = None,
    ) -> tuple[
        FailureAnalysis,
        DebugSuggestion,
        PlanStep | None,
    ]:
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

        file_tool = FileTool(workspace=workspace)

        workspace_snapshot: list[dict] = []

        for item in file_tool.list_directory():
            if item["type"] == "file":
                workspace_snapshot.append(
                {
                    "path": item["path"],
                    "content": file_tool.read_file(item["path"]),
                }
            )

        suggestion = self.debug_agent.analyze(
            failure=failure,
            history=history,
            workspace_snapshot=workspace_snapshot,
        )
        

        logger.info("Debug Suggestion | " f"Summary={suggestion.summary}")

        self.patch_applier.apply(
            suggestion=suggestion,
            workspace=workspace,
        )   
        if (
            not suggestion.files
            and not suggestion.commands
            and not suggestion.dependencies
        ):
            logger.warning("Gemini returned no executable fix.")

        logger.info(
            "AI returned %d file patch(es), %d command patch(es), %d dependency patch(es)",
            len(suggestion.files),
            len(suggestion.commands),
            len(suggestion.dependencies),
        )

        for patch in suggestion.files:
            logger.info(
                "Patch: %s (%d chars)",
                patch.path,
                len(patch.content),
            )

        patched_step = step

        if step is not None:
            patched_step = self.patch_applier.apply_command_patches(
                suggestion=suggestion,
                step=step,
            )

        return analysis, suggestion, patched_step
