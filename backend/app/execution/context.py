from dataclasses import dataclass
from pathlib import Path

from app.models.execution import Execution


@dataclass
class ExecutionContext:
    """
    Shared execution state.

    This object will grow as the execution engine
    gains more capabilities.
    """

    workspace: Path

    session_id: str

    plan_id: int

    execution: Execution | None = None
