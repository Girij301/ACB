from pathlib import Path

from app.core.config import WORKSPACE_DIR


def get_safe_path(
    relative_path: str,
    workspace: Path | None = None,
) -> Path:
    """
    Resolve a user-provided path safely inside the workspace.

    Args:
        relative_path: Path relative to the workspace.
        workspace: Optional workspace directory.
                   Defaults to settings.WORKSPACE_DIR.

    Raises:
        ValueError: If the resolved path is outside the workspace.
    """

    workspace = (workspace or WORKSPACE_DIR).resolve()

    target = (workspace / relative_path).resolve()

    if workspace not in target.parents and target != workspace:
        raise ValueError("Path is outside the workspace.")

    return target
