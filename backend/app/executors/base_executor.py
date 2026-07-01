from abc import ABC, abstractmethod


class BaseExecutor(ABC):
    """
    Abstract base class for command executors.

    Every executor (Local, Docker, SSH, etc.)
    must implement the run() method.
    """

    @abstractmethod
    def run(
        self,
        command: str,
        cwd: str = ".",
        timeout: int = 60,
    ) -> dict:

        pass
