from app.tools.terminal_tool import TerminalTool


class TerminalService:
    """
    Service layer for terminal execution.
    """

    def __init__(self):
        self.terminal_tool = TerminalTool()

    def execute_command(
        self,
        command: str,
        cwd: str = ".",
        timeout: int = 60,
    ):
        return self.terminal_tool.run(
            command=command,
            cwd=cwd,
            timeout=timeout,
        )
