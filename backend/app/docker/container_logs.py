from dataclasses import dataclass


@dataclass(slots=True)
class ContainerLogs:
    """
    Captured output from a Docker container.
    """

    stdout: str
    stderr: str
