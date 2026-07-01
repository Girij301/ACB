from app.executors.local_executor import LocalExecutor


class TerminalTool:
    """
    Tool responsible for terminal execution.

    It delegates the actual execution to an Executor.
    """

    def __init__(self):
        self.executor = LocalExecutor()

    def run(
        self,
        command: str,
        cwd: str = ".",
        timeout: int = 60,
    ) -> dict:
        """
        Execute a command using the configured executor.
        """

        return self.executor.run(
            command=command,
            cwd=cwd,
            timeout=timeout,
        )
