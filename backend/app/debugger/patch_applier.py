from pathlib import Path

from app.schemas.debug import DebugSuggestion
from app.schemas.planner import PlanStep
from app.tools.file_tool import FileTool
from app.core.logger import logger

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
                logger.info("Applying patch to %s", patch.path)

            else:
                file_tool.create_file(
                    relative_path=patch.path,
                    content=patch.content,
                )
                logger.info("Updated %s", patch.path)
                logger.info("Created %s", patch.path)
    def apply_command_patches(
        self,
        suggestion: DebugSuggestion,
        step: PlanStep,
    ) -> PlanStep:
        """
        Apply AI-generated command replacements
        to the current plan step.
        """

        updated_parameters = dict(step.parameters)

        # Patch terminal commands
        command = updated_parameters.get("command")

        if command:
            for patch in suggestion.commands:
                if patch.old == command:
                    updated_parameters["command"] = patch.new

        # Remove invalid parameter for append_file
        if (
            step.action.value == "append_file"
            and "goal" in updated_parameters
        ):
            updated_parameters.pop("goal")

        return step.model_copy(
            update={
                "parameters": updated_parameters,
            }
        )
