from dataclasses import dataclass

from app.docker.execution_info import ExecutionInfo


@dataclass(slots=True)
class ExecutionResult:
    """
    Represents the result of executing a command
    inside a Docker container.
    """

    stdout: str
    stderr: str
    exit_code: int
    execution_time: float
    success: bool
    execution_info: ExecutionInfo | None = None
