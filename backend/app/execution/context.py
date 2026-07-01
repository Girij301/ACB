from dataclasses import dataclass
from pathlib import Path


@dataclass
class ExecutionContext:
    """
    Shared execution state.
    This object will grow as the execution engine
    gains more capabilities.
    """

    workspace: Path
    plan_id: int
