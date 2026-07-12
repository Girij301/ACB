from app.services.generation_service import CodeGenerationService
from app.tools.file_tool import FileTool


class WriteFileHandler:
    def __init__(self, file_tool: FileTool):
        self.file_tool = file_tool
        self.generator = CodeGenerationService()

    def execute(
        self,
        relative_path: str,
        goal: str,
        step_description: str,
    ):
        code = self.generator.generate(
            goal=goal,
            step_description=step_description,
            relative_path=relative_path,
        )

        return self.file_tool.write_file(
            relative_path=relative_path,
            content=code,
        )