from dataclasses import dataclass
from pathlib import Path

from app.docker.execution_container import ExecutionContainer
from app.models.execution import Execution


@dataclass
class ExecutionContext:
    """
    Shared execution state.

    This object is passed throughout the execution
    pipeline and stores resources shared by every
    execution step.
    """

    workspace: Path

    session_id: str

    plan_id: int

    execution: Execution | None = None

    # Persistent Docker container used during
    # the lifetime of this execution.
    container: ExecutionContainer | None = None
