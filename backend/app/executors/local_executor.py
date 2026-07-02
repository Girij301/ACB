import subprocess
import time

from app.executors.base_executor import BaseExecutor
from app.utils.path_utils import get_safe_path


class LocalExecutor(BaseExecutor):
    """
    Executes terminal commands on the local machine.
    """

    def run(
        self,
        command: str,
        cwd: str = ".",
        timeout: int = 60,
    ) -> dict:

        working_directory = get_safe_path(cwd)

        if not working_directory.exists():
            raise FileNotFoundError(f"Directory '{cwd}' does not exist.")

        if not working_directory.is_dir():
            raise NotADirectoryError(f"'{cwd}' is not a directory.")

        start_time = time.perf_counter()

        try:
            result = subprocess.run(
                command,
                cwd=working_directory,
                capture_output=True,
                text=True,
                timeout=timeout,
                shell=True,
            )

            execution_time = time.perf_counter() - start_time

            return {
                "success": result.returncode == 0,
                "action": "run_terminal",
                "command": command,
                "cwd": cwd,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode,
                "execution_time": round(execution_time, 3),
            }

        except subprocess.TimeoutExpired:
            execution_time = time.perf_counter() - start_time

            return {
                "success": False,
                "action": "run_terminal",
                "error_type": "TimeoutExpired",
                "command": command,
                "cwd": cwd,
                "stdout": "",
                "stderr": f"Command timed out after {timeout} seconds.",
                "exit_code": -1,
                "execution_time": round(execution_time, 3),
            }

        except FileNotFoundError:
            execution_time = time.perf_counter() - start_time

            return {
                "success": False,
                "action": "run_terminal",
                "error_type": "FileNotFoundError",
                "command": command,
                "cwd": cwd,
                "stdout": "",
                "stderr": "Command not found.",
                "exit_code": -1,
                "execution_time": round(execution_time, 3),
            }

        except Exception as e:
            execution_time = time.perf_counter() - start_time

            return {
                "success": False,
                "action": "run_terminal",
                "error_type": type(e).__name__,
                "command": command,
                "cwd": cwd,
                "stdout": "",
                "stderr": str(e),
                "exit_code": -1,
                "execution_time": round(execution_time, 3),
            }