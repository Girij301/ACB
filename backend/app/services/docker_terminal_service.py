from app.execution.context import ExecutionContext
from app.tools.terminal_tool import TerminalTool


class DockerTerminalService:
    """
    Executes terminal commands.

    If a Docker container exists in the execution context,
    commands are executed inside Docker.

    Otherwise, commands are executed locally. This preserves
    compatibility with the existing execution engine and tests.
    """

    def __init__(self) -> None:
        self.local_terminal = TerminalTool()

    def execute_command(
        self,
        context: ExecutionContext,
        command: str,
        cwd: str | None = None,
        timeout: int | None = None,
    ):
        """
        Execute a shell command using the appropriate backend.
        """

        # Docker execution
        if context.container is not None:
            return context.container.execute(command)

        # Local execution
        return self.local_terminal.run(
            command=command,
            cwd=cwd,
            timeout=timeout,
        )
