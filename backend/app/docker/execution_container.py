from __future__ import annotations

from app.docker.docker_manager import DockerManager
from app.docker.exec_result import ExecResult
from app.docker.types import ContainerConfig
from docker.models.containers import Container


class ExecutionContainer:
    """
    Represents a persistent execution container.

    One instance owns one Docker container for the
    lifetime of a single execution.

    The ExecutionEngine will create one
    ExecutionContainer and reuse it for every
    terminal command in the execution plan.
    """

    def __init__(
        self,
        docker_manager: DockerManager,
        config: ContainerConfig,
    ) -> None:
        self.docker = docker_manager
        self.config = config

        self._container: Container | None = None

    @property
    def container(self) -> Container:
        """
        Returns the underlying Docker container.

        Raises an exception if the container
        has not been created yet.
        """

        if self._container is None:
            raise RuntimeError("Execution container has not been created.")

        return self._container

    @property
    def id(self) -> str:
        """
        Docker container id.
        """

        return self.container.id

    def create(self) -> None:
        """
        Create the Docker container.

        The container is created but not started.
        """

        if self._container is not None:
            return

        self._container = self.docker.create_container(
            self.config,
        )

    def start(self) -> None:
        """
        Start the container.
        """

        self.docker.start_container(
            self.id,
        )

    def stop(self) -> None:
        """
        Stop the container.
        """

        self.docker.stop_container(
            self.id,
        )

    def remove(self) -> None:
        """
        Remove the container.
        """

        self.docker.remove_container(
            self.id,
            force=True,
        )

        self._container = None

    def close(self) -> None:
        """
        Cleanup helper.

        Safe to call multiple times.
        """

        if self._container is None:
            return

        try:
            self.stop()
        except Exception:
            pass

        try:
            self.remove()
        except Exception:
            pass

    def execute(
        self,
        command: str,
    ) -> ExecResult:
        """
        Execute a command inside
        the running container.
        """

        if self.id is None:
            raise RuntimeError("Container has not been created.")

        return self.docker.exec_run(
            self.id,
            command,
        )
