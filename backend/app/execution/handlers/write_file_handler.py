from app.services.generation_service import CodeGenerationService
from app.tools.file_tool import FileTool


class WriteFileHandler:
    def __init__(self, file_tool: FileTool):
        self.file_tool = file_tool
        self.generator = CodeGenerationService()

    def execute(
        self,
        relative_path: str,
        content: str | None = None,
        goal: str | None = None,
        step_description: str | None = None,
    ):
        """
        Write content to an existing file.

        If explicit content is provided, write it directly.
        Otherwise, generate the content using the AI generation service.
        """

        if content is None:
            if not goal:
                raise ValueError(
                    "Either 'content' or 'goal' must be provided."
                )

            content = self.generator.generate(
                goal=goal,
                step_description=step_description or "",
                relative_path=relative_path,
            )

        return self.file_tool.write_file(
            relative_path=relative_path,
            content=content,
        )