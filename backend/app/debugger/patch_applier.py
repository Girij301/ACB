from pathlib import Path

from app.schemas.debug import DebugSuggestion
from app.schemas.planner import PlanStep
from app.tools.file_tool import FileTool


class PatchApplier:
    """
    Applies AI-generated patches to the workspace
    and execution plan.
    """

    def apply(
        self,
        suggestion: DebugSuggestion,
        workspace: Path,
    ) -> None:
        """
        Apply all file modifications.
        """

        file_tool = FileTool(
            workspace=workspace,
        )

        for patch in suggestion.files:

            if file_tool.exists(patch.path):
                file_tool.write_file(
                    relative_path=patch.path,
                    content=patch.content,
                )

            else:
                file_tool.create_file(
                    relative_path=patch.path,
                    content=patch.content,
                )

    def apply_command_patches(
        self,
        suggestion: DebugSuggestion,
        step: PlanStep,
    ) -> PlanStep:
        """
        Apply AI-generated command replacements
        to the current plan step.
        """

        command = step.parameters.get("command")

        if not command:
            return step

        for patch in suggestion.commands:

            if patch.old == command:

                updated_parameters = {
                    **step.parameters,
                    "command": patch.new,
                }

                return step.model_copy(
                    update={
                        "parameters": updated_parameters,
                    }
                )

        return step