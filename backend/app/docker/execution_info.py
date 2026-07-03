from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionInfo:
    """
    Metadata describing a single Docker execution.
    """

    container_id: str

    image: str

    exit_code: int

    execution_time: float

    timed_out: bool

    memory_limit: str | None

    nano_cpus: int | None
