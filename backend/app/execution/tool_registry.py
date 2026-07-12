from app.execution.context import ExecutionContext
from app.execution.handlers.write_file_handler import WriteFileHandler
from app.schemas.planner import ActionType, PlanStep
from app.services.docker_terminal_service import DockerTerminalService
from app.tools.file_tool import FileTool


class ToolRegistry:
    """
    Maps plan actions to executable tool handlers.
    """

    def __init__(
        self,
        context: ExecutionContext,
        terminal_service: DockerTerminalService | None = None,
    ) -> None:

        self.context = context

        self.file_tool = FileTool(
            workspace=context.workspace,
        )

        self.write_file_handler = WriteFileHandler(self.file_tool)

        self.terminal_service = terminal_service or DockerTerminalService()

    def get_handler(
        self,
        step: PlanStep,
    ):
        handlers = {
            ActionType.CREATE_DIRECTORY: (
                lambda: self.file_tool.create_directory(**step.parameters)
            ),
            ActionType.CREATE_FILE: (
                lambda: self.file_tool.create_file(**step.parameters)
            ),
            ActionType.WRITE_FILE: (
                lambda: self.write_file_handler.execute(
                    relative_path=step.parameters["relative_path"],
                    goal=step.goal,
                    step_description=step.description,
                )
            ),
            ActionType.APPEND_FILE: (
                lambda: self.file_tool.append_file(**step.parameters)
            ),
            ActionType.READ_FILE: (lambda: self.file_tool.read_file(**step.parameters)),
            ActionType.DELETE_FILE: (
                lambda: self.file_tool.delete_file(**step.parameters)
            ),
            ActionType.LIST_DIRECTORY: (
                lambda: self.file_tool.list_directory(**step.parameters)
            ),
            ActionType.RUN_TERMINAL: (
                lambda: self.terminal_service.execute_command(
                    context=self.context,
                    **step.parameters,
                )
            ),
        }

        return handlers.get(step.action)
