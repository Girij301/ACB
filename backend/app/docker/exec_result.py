from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ExecResult:
    """
    Result of executing a command
    inside an existing container.
    """

    exit_code: int
    stdout: str
    stderr: str

    execution_time: float = 0.0
    execution_info: Any | None = None

    @property
    def success(self) -> bool:
        return self.exit_code == 0
