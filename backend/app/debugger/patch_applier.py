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
        cwd: str | None = None,
    ) -> None:
        """
        Apply all file modifications.
        """

        file_tool = FileTool(
            workspace=workspace,
        )

        for patch in suggestion.files:

            relative_path = patch.path

            if not file_tool.exists(relative_path) and cwd:
                candidate = f"{cwd.rstrip('/')}/{relative_path.lstrip('/')}"
                if file_tool.exists(candidate):
                    relative_path = candidate

            if file_tool.exists(relative_path):
                file_tool.write_file(
                    relative_path=relative_path,
                    content=patch.content,
                )
                logger.info("Updated %s", relative_path)

            else:
                if cwd and not relative_path.startswith(cwd):
                    relative_path = f"{cwd.rstrip('/')}/{relative_path.lstrip('/')}"

                file_tool.create_file(
                    relative_path=relative_path,
                    content=patch.content,
                )
                logger.info("Created %s", relative_path)
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
