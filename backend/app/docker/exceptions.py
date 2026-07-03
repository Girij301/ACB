from app.core.exceptions import AppException


class DockerException(AppException):
    """
    Base exception for all Docker-related errors.
    """

    pass


class DockerUnavailableError(DockerException):
    """
    Raised when Docker is not installed,
    not running, or cannot be reached.
    """

    def __init__(self):
        super().__init__("Docker daemon is unavailable.")


class ContainerCreationError(DockerException):
    """
    Raised when a Docker container
    cannot be created.
    """

    def __init__(self, reason: str):
        super().__init__(f"Failed to create Docker container: {reason}")


class ContainerStartError(DockerException):
    """
    Raised when a Docker container
    fails to start.
    """

    def __init__(self, container_name: str):
        super().__init__(f"Failed to start container '{container_name}'.")


class ContainerStopError(DockerException):
    """
    Raised when a Docker container
    cannot be stopped.
    """

    def __init__(self, container_name: str):
        super().__init__(f"Failed to stop container '{container_name}'.")


class ContainerRemovalError(DockerException):
    """
    Raised when a Docker container
    cannot be removed.
    """

    def __init__(self, container_name: str):
        super().__init__(f"Failed to remove container '{container_name}'.")


class ContainerNotFoundError(DockerException):
    """
    Raised when a requested Docker
    container does not exist.
    """

    def __init__(self, container_name: str):
        super().__init__(f"Container '{container_name}' was not found.")


class ContainerWaitError(DockerException):
    """
    Raised when waiting for a container fails.
    """

    def __init__(self, container_name: str):
        super().__init__(f"Failed while waiting for container '{container_name}'.")


class ContainerLogsError(DockerException):
    """
    Raised when container logs cannot be retrieved.
    """

    def __init__(self, container_name: str):
        super().__init__(f"Failed to retrieve logs from container '{container_name}'.")


class ImagePullError(DockerException):
    """
    Raised when a Docker image
    cannot be pulled.
    """

    def __init__(self, image: str):
        super().__init__(f"Failed to pull Docker image '{image}'.")


class ImageNotFoundError(DockerException):
    """
    Raised when a Docker image
    does not exist.
    """

    def __init__(self, image: str):
        super().__init__(f"Docker image '{image}' was not found.")


class ImageRemovalError(DockerException):
    """
    Raised when a Docker image
    cannot be removed.
    """

    def __init__(self, image: str):
        super().__init__(f"Failed to remove Docker image '{image}'.")
