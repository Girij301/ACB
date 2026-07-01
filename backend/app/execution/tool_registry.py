from app.execution.context import ExecutionContext
from app.schemas.planner import ActionType, PlanStep
from app.tools.file_tool import FileTool
from app.tools.terminal_tool import TerminalTool


class ToolRegistry:
    """
    Maps plan actions to executable tool handlers.
    """

    def __init__(
        self,
        context: ExecutionContext,
        terminal_tool: TerminalTool | None = None,
    ) -> None:

        self.file_tool = FileTool(
            workspace=context.workspace,
        )

        self.terminal_tool = terminal_tool or TerminalTool()

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
                lambda: self.file_tool.write_file(**step.parameters)
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
                lambda: self.terminal_tool.run(**step.parameters)
            ),
        }

        return handlers.get(step.action)
