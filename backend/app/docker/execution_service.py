from app.docker.docker_manager import DockerManager
from app.docker.execution_result import ExecutionResult
from app.docker.sandbox import DEFAULT_SANDBOX


class DockerExecutionService:
    """
    High-level service responsible for executing
    commands inside the Docker sandbox.
    """

    def __init__(
        self,
        docker_manager: DockerManager,
    ) -> None:
        self._docker = docker_manager

    def execute(
        self,
        command: list[str],
    ) -> ExecutionResult:
        """
        Execute a command inside the default sandbox.
        """

        config = DEFAULT_SANDBOX.to_container_config()

        self._docker.ensure_image(config.image)

        return self._docker.execute(
            config=config,
            command=command,
        )
