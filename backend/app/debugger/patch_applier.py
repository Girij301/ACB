from pathlib import Path

from app.schemas.debug import DebugSuggestion
from app.tools.file_tool import FileTool


class PatchApplier:
    """
    Applies AI-generated patches to the workspace.
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
