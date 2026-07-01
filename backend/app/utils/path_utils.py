from pathlib import Path

from app.core.config import settings


def get_safe_path(relative_path: str) -> Path:
    """
    Resolve a user-provided path safely inside the workspace.

    Raises:
        ValueError: If the resolved path is outside the workspace.
    """
    workspace = settings.WORKSPACE_DIR.resolve()
    target = (workspace / relative_path).resolve()

    if workspace not in target.parents and target != workspace:
        raise ValueError("Path is outside the workspace.")

    return target
