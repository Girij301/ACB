from __future__ import annotations

import time
from time import perf_counter
from typing import Optional

import docker
from app.core.logger import logger
from app.docker.container_logs import ContainerLogs
from app.docker.exceptions import (
    ContainerLogsError,
    ContainerNotFoundError,
    ContainerWaitError,
    DockerUnavailableError,
    ImageNotFoundError,
    ImagePullError,
    ImageRemovalError,
)
from app.docker.exec_result import ExecResult
from app.docker.execution_info import ExecutionInfo
from app.docker.execution_result import ExecutionResult
from app.docker.types import ContainerConfig
from docker.client import DockerClient
from docker.errors import APIError, DockerException, ImageNotFound, NotFound
from docker.models.containers import Container
from docker.models.images import Image


class DockerManager:
    """
    Manages the connection to the Docker daemon.

    Responsibilities:
    - Create and manage the Docker client
    - Verify Docker availability
    - Create containers
    - Start containers
    - Stop containers
    - Remove containers
    - Lookup containers

    Higher-level execution logic will be added
    in later phases.
    """

    def __init__(self) -> None:
        self._client: Optional[DockerClient] = None

    @property
    def client(self) -> DockerClient:
        """
        Lazily create the Docker client.
        """

        if self._client is None:
            self._client = docker.from_env()

        return self._client

    def is_available(self) -> bool:
        """
        Returns True if Docker is reachable.
        """

        try:
            self.client.ping()
            return True

        except DockerException:
            return False

    def ensure_available(self) -> None:
        """
        Raises an exception if Docker
        is unavailable.
        """

        if not self.is_available():
            raise DockerUnavailableError()

    # Container Lifecycle

    def create_container(
        self,
        config: ContainerConfig,
        command: Optional[list[str]] = None,
    ) -> Container:
        """
        Create a Docker container.

        The container is created but NOT started.
        """

        self.ensure_available()

        self.ensure_image(config.image)

        logger.info(
            "Creating Docker container using image '%s'.",
            config.image,
        )

        container = self.client.containers.create(
            image=config.image,
            command=command if command is not None else config.command,
            working_dir=config.working_directory,
            volumes={
                str(config.workspace_host): {
                    "bind": config.workspace_container,
                    "mode": "rw",
                }
            },
            environment=config.environment,
            network_disabled=config.network_disabled,
            detach=True,
            tty=config.tty,
            stdin_open=config.stdin_open,
            mem_limit=config.memory_limit,
            nano_cpus=config.nano_cpus,
            auto_remove=config.auto_remove,
        )

        logger.info(
            "Container created: %s",
            container.id,
        )

        return container

    def get_container(
        self,
        container_id: str,
    ) -> Optional[Container]:
        """
        Retrieve a container by ID.

        Returns None if it does not exist.
        """

        self.ensure_available()

        try:
            return self.client.containers.get(container_id)

        except NotFound:
            return None

    def start_container(
        self,
        container_id: str,
    ) -> None:
        """
        Start an existing container.
        """

        container = self.get_container(container_id)

        if container is None:
            raise ContainerNotFoundError(container_id)

        logger.info(
            "Starting container %s",
            container.id,
        )

        container.start()

    def stop_container(
        self,
        container_id: str,
        timeout: int = 10,
    ) -> None:
        """
        Stop a running container.
        """

        container = self.get_container(container_id)

        if container is None:
            raise ContainerNotFoundError(container_id)

        logger.info(
            "Stopping container %s",
            container.id,
        )

        container.stop(timeout=timeout)

    def remove_container(
        self,
        container_id: str,
        force: bool = False,
    ) -> None:
        """
        Remove an existing container.
        """

        container = self.get_container(container_id)

        if container is None:
            return

        logger.info(
            "Removing container %s",
            container.id,
        )

        container.remove(force=force)

    def wait_container(
        self,
        container_id: str,
        timeout: int,
    ) -> int:
        """
        Wait until the container exits.

        Returns the exit status code.
        """

        container = self.get_container(container_id)

        if container is None:
            raise ContainerNotFoundError(container_id)

        logger.info(
            "Waiting for container %s",
            container.id,
        )

        try:
            result = container.wait(timeout=timeout)

        except APIError as exc:
            raise ContainerWaitError(container.id) from exc

        return int(result["StatusCode"])

    def get_logs(
        self,
        container_id: str,
    ) -> ContainerLogs:
        """
        Return stdout and stderr separately.
        """

        container = self.get_container(container_id)

        if container is None:
            raise ContainerNotFoundError(container_id)

        try:
            stdout = container.logs(
                stdout=True,
                stderr=False,
            ).decode("utf-8")

            stderr = container.logs(
                stdout=False,
                stderr=True,
            ).decode("utf-8")

        except APIError as exc:
            raise ContainerLogsError(container.id) from exc

        return ContainerLogs(
            stdout=stdout,
            stderr=stderr,
        )

    def exec_run(
        self,
        container_id: str,
        command: str,
        cwd: str | None = None,
    ) -> ExecResult:
        """
        Execute a command inside
        an already-running container.
        """

        container = self.get_container(container_id)

        if container is None:
            raise ContainerNotFoundError(container_id)

        start = perf_counter()

        # Resolve working directory inside the container.
        workdir = None

        if cwd:
            workdir = f"/workspace/{cwd.strip('/')}"

        logger.info(
            "Executing inside container %s (cwd=%s): %s",
            container.id,
            workdir or "/workspace",
            command,
        )

        exec_result = container.exec_run(
            [
                "sh",
                "-c",
                command,
            ],
            stdout=True,
            stderr=True,
            workdir=workdir,
        )   

        elapsed = perf_counter() - start

        output = exec_result.output.decode(
            "utf-8",
            errors="ignore",
        )

        return ExecResult(
            exit_code=exec_result.exit_code,
            stdout=output if exec_result.exit_code == 0 else "",
            stderr="" if exec_result.exit_code == 0 else output,
            execution_time=elapsed,
        )

    def get_exit_code(
        self,
        container_id: str,
    ) -> int:
        """
        Retrieve the container exit code.
        """

        container = self.get_container(container_id)

        if container is None:
            raise ContainerNotFoundError(container_id)

        container.reload()

        return int(container.attrs["State"]["ExitCode"])

    def execute(
        self,
        config: ContainerConfig,
    ) -> ExecutionResult:
        """
        Full sandbox execution lifecycle.

        Creates a container, starts it, waits for completion,
        collects logs, records execution metadata, and ensures
        cleanup even if execution fails.
        """

        self.ensure_available()

        container = self.create_container(config)

        start_time = time.time()

        timed_out = False

        try:
            logger.info(
                "Starting container %s",
                container.id,
            )

            container.start()

            logger.info(
                "Waiting for container %s",
                container.id,
            )

            try:
                result = container.wait(
                    timeout=config.timeout,
                )

            except Exception:
                logger.warning(
                    "Container %s exceeded timeout (%ss).",
                    container.id,
                    config.timeout,
                )

                container.stop(timeout=1)

                timed_out = True

                result = {
                    "StatusCode": -1,
                }

            exit_code = int(result.get("StatusCode", 1))

            logs = container.logs(
                stdout=True,
                stderr=True,
            ).decode("utf-8")

            execution_time = time.time() - start_time

            success = exit_code == 0 and not timed_out

            stdout = logs if success else ""

            if timed_out:
                stderr = f"Execution exceeded timeout " f"of {config.timeout} seconds."
            else:
                stderr = "" if success else logs

            return ExecutionResult(
                stdout=stdout,
                stderr=stderr,
                exit_code=exit_code,
                execution_time=execution_time,
                success=success,
                execution_info=ExecutionInfo(
                    container_id=container.id,
                    image=config.image,
                    exit_code=exit_code,
                    execution_time=execution_time,
                    timed_out=timed_out,
                    memory_limit=config.memory_limit,
                    nano_cpus=config.nano_cpus,
                ),
            )

        finally:
            logger.info(
                "Removing container %s",
                container.id,
            )

            try:
                container.remove(force=True)

            except Exception:
                logger.exception(
                    "Failed to remove container %s",
                    container.id,
                )

    def container_exists(
        self,
        container_id: str,
    ) -> bool:
        """
        Check whether a container exists.
        """

        return self.get_container(container_id) is not None

    # Image Management

    def image_exists(
        self,
        image: str,
    ) -> bool:
        """
        Returns True if the image
        exists locally.
        """

        self.ensure_available()

        try:
            self.client.images.get(image)
            return True

        except ImageNotFound:
            return False

    def get_image(
        self,
        image: str,
    ) -> Image:
        """
        Retrieve an image.

        Raises ImageNotFoundError
        if the image does not exist.
        """

        self.ensure_available()

        try:
            return self.client.images.get(image)

        except ImageNotFound:
            raise ImageNotFoundError(image)

    def pull_image(
        self,
        image: str,
    ) -> Image:
        """
        Pull an image from the registry.
        """

        self.ensure_available()

        logger.info(
            "Pulling Docker image '%s'.",
            image,
        )

        try:
            return self.client.images.pull(image)

        except APIError as exc:
            raise ImagePullError(image) from exc

    def ensure_image(
        self,
        image: str,
    ) -> Image:
        """
        Ensure that the image exists locally.

        Pulls it automatically if missing.
        """

        if self.image_exists(image):
            logger.info(
                "Docker image '%s' already exists.",
                image,
            )
            return self.get_image(image)

        logger.info(
            "Docker image '%s' not found locally. Pulling...",
            image,
        )

        return self.pull_image(image)

    def remove_image(
        self,
        image: str,
        force: bool = False,
    ) -> None:
        """
        Remove an image from the local cache.
        """

        self.ensure_available()

        logger.info(
            "Removing Docker image '%s'.",
            image,
        )

        try:
            self.client.images.remove(
                image=image,
                force=force,
            )

        except ImageNotFound:
            raise ImageNotFoundError(image)

        except APIError as exc:
            raise ImageRemovalError(image) from exc

    # Cleanup

    def close(self) -> None:
        """
        Close the Docker client.
        """

        if self._client is not None:
            try:
                self._client.close()
                logger.info("Docker client closed.")

            finally:
                self._client = None
