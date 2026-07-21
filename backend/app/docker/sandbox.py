from dataclasses import dataclass
from pathlib import Path

from app.core.config import WORKSPACE_DIR, settings
from app.docker.types import ContainerConfig


@dataclass(frozen=True)
class SandboxConfig:
    """
    Immutable configuration describing a Docker sandbox.
    """

    image: str

    workspace_host: Path
    workspace_container: str
    working_directory: str

    command: str | list[str] | None

    timeout: int

    environment: dict[str, str]

    memory_limit: str | None

    nano_cpus: int | None

    network_disabled: bool

    auto_remove: bool

    tty: bool

    stdin_open: bool

    def to_container_config(
        self,
        workspace_host: Path | None = None,
    ) -> ContainerConfig:
        return ContainerConfig(
            image=self.image,
            workspace_host=workspace_host or self.workspace_host,
            workspace_container=self.workspace_container,
            working_directory=self.working_directory,
            command=self.command,
            timeout=self.timeout,
            environment=self.environment,
            memory_limit=self.memory_limit,
            nano_cpus=self.nano_cpus,
            network_disabled=self.network_disabled,
            auto_remove=self.auto_remove,
            tty=self.tty,
            stdin_open=self.stdin_open,
            workspace_volume="acb_workspace",
        )


DEFAULT_SANDBOX = SandboxConfig(
    image=settings.DOCKER_IMAGE,
    workspace_host=WORKSPACE_DIR,
    workspace_container="/workspace",
    working_directory=settings.DOCKER_WORKDIR,
    command=[
        "tail",
        "-f",
        "/dev/null",
    ],
    timeout=30,
    environment={},
    memory_limit=settings.DOCKER_MEMORY_LIMIT,
    nano_cpus=settings.DOCKER_NANO_CPUS,
    network_disabled=settings.DOCKER_NETWORK_DISABLED,
    auto_remove=settings.DOCKER_AUTO_REMOVE,
    tty=False,
    stdin_open=False,
)
