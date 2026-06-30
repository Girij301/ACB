from pydantic import BaseModel


class CreateFileRequest(BaseModel):
    path: str
    content: str = ""


class ReadFileRequest(BaseModel):
    path: str


class WriteFileRequest(BaseModel):
    path: str
    content: str


class AppendFileRequest(BaseModel):
    path: str
    content: str


class DeleteFileRequest(BaseModel):
    path: str


class CreateDirectoryRequest(BaseModel):
    path: str


class ListDirectoryRequest(BaseModel):
    path: str = ""


class ExistsRequest(BaseModel):
    path: str
