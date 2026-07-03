from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class ContainerStatus(str, Enum):
    """
    Represents the lifecycle state
    of a Docker container.
    """

    CREATED = "created"
    RUNNING = "running"
    EXITED = "exited"
    REMOVED = "removed"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ContainerConfig:
    """
    Immutable configuration used to create
    a Docker container.

    This object contains everything required
    to build an isolated execution environment.
    """

    # Image

    image: str

    # Workspace

    workspace_host: Path

    workspace_container: str

    working_directory: str

    # Execution

    command: list[str] | None = None

    timeout: int = 30

    environment: dict[str, str] = field(default_factory=dict)

    # Resources

    memory_limit: str | None = None

    nano_cpus: int | None = None

    # Security

    network_disabled: bool = True

    # Runtime

    auto_remove: bool = True

    tty: bool = False

    stdin_open: bool = False


@dataclass
class ContainerInfo:
    """
    Public representation of a Docker container.

    Docker SDK objects should never leave
    DockerManager.
    """

    id: str

    name: str

    image: str

    status: ContainerStatus
