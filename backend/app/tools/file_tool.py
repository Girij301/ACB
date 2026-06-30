from pathlib import Path

from app.core.config import settings


def get_safe_path(relative_path: str) -> Path:
    
    #Resolve a user-provided path safely inside the workspace.

    #Raises:ValueError: If the resolved path is outside the workspace.
    workspace = settings.WORKSPACE_DIR.resolve()
    target = (workspace / relative_path).resolve()

    if workspace not in target.parents and target != workspace:
        raise ValueError("Path is outside the workspace.")

    return target

"""Provides safe filesystem operations inside the workspace."""
class FileTool:

    def create_file(self, relative_path: str, content: str = "") -> Path:
    
        file_path = get_safe_path(relative_path)

        if file_path.exists():
            raise FileExistsError(f"File '{relative_path}' already exists.")

        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")

        return file_path
    
    def read_file(self, relative_path: str) -> str:
        
        file_path = get_safe_path(relative_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File '{relative_path}' does not exist.")

        return file_path.read_text(encoding="utf-8")
    
    def write_file(self, relative_path: str, content: str) -> Path:
    
        file_path = get_safe_path(relative_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File '{relative_path}' does not exist.")

        file_path.write_text(content, encoding="utf-8")

        return file_path
    
    def append_file(self, relative_path: str, content: str) -> Path:
    
        file_path = get_safe_path(relative_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File '{relative_path}' does not exist.")

        with file_path.open("a", encoding="utf-8") as file:
            file.write(content)

        return file_path
    
    def delete_file(self, relative_path: str) -> Path:
   
        file_path = get_safe_path(relative_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File '{relative_path}' does not exist.")

        if not file_path.is_file():
            raise IsADirectoryError(f"'{relative_path}' is not a file.")

        file_path.unlink()

        return file_path
    
    def create_directory(self, relative_path: str) -> Path:
    
        directory_path = get_safe_path(relative_path)

        if directory_path.exists():
            raise FileExistsError(
                f"Directory '{relative_path}' already exists."
            )

        directory_path.mkdir(parents=True)

        return directory_path
    
    def list_directory(self, relative_path: str = "") -> list[dict]:
    
        directory_path = get_safe_path(relative_path)

        if not directory_path.exists():
            raise FileNotFoundError(
                f"Directory '{relative_path}' does not exist."
            )

        if not directory_path.is_dir():
            raise NotADirectoryError(
                f"'{relative_path}' is not a directory."
            )

        items = []

        for item in directory_path.iterdir():
            items.append(
                {
                    "name": item.name,
                    "type": "directory" if item.is_dir() else "file",
                    "path": str(item.relative_to(settings.WORKSPACE_DIR))
                }
            )

        return items
    
    def exists(self, relative_path: str) -> bool:
    
        path = get_safe_path(relative_path)
        return path.exists()
