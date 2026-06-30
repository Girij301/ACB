from app.tools.file_tool import FileTool


class FileService:
    """
    Service layer for file operations.
    """

    def __init__(self):
        self.file_tool = FileTool()

    def create_file(self, path: str, content: str = ""):
        return self.file_tool.create_file(path, content)

    def read_file(self, path: str):
        return self.file_tool.read_file(path)

    def write_file(self, path: str, content: str):
        return self.file_tool.write_file(path, content)

    def append_file(self, path: str, content: str):
        return self.file_tool.append_file(path, content)

    def delete_file(self, path: str):
        return self.file_tool.delete_file(path)

    def create_directory(self, path: str):
        return self.file_tool.create_directory(path)

    def list_directory(self, path: str = ""):
        return self.file_tool.list_directory(path)

    def exists(self, path: str):
        return self.file_tool.exists(path)
