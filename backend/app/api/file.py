from fastapi import APIRouter

from app.schemas.common import ToolResponse
from app.schemas.file_schemas import (
    AppendFileRequest,
    CreateDirectoryRequest,
    CreateFileRequest,
    DeleteFileRequest,
    ExistsRequest,
    ListDirectoryRequest,
    ReadFileRequest,
    WriteFileRequest,
)
from app.services.file_service import FileService

router = APIRouter(prefix="/files", tags=["File Tools"])

service = FileService()


@router.post("/create", response_model=ToolResponse)
def create_file(request: CreateFileRequest):
    path = service.create_file(request.path, request.content)

    return ToolResponse(
        success=True,
        message="File created successfully.",
        data={"path": str(path)},
    )


@router.post("/read", response_model=ToolResponse)
def read_file(request: ReadFileRequest):
    content = service.read_file(request.path)

    return ToolResponse(
        success=True,
        message="File read successfully.",
        data={"content": content},
    )


@router.post("/write", response_model=ToolResponse)
def write_file(request: WriteFileRequest):

    path = service.write_file(
        request.path,
        request.content,
    )

    return ToolResponse(
        success=True,
        message="File written successfully.",
        data={"path": str(path)},
    )


@router.post("/append", response_model=ToolResponse)
def append_file(request: AppendFileRequest):

    path = service.append_file(
        request.path,
        request.content,
    )

    return ToolResponse(
        success=True,
        message="Content appended successfully.",
        data={"path": str(path)},
    )


@router.post("/delete", response_model=ToolResponse)
def delete_file(request: DeleteFileRequest):

    path = service.delete_file(request.path)

    return ToolResponse(
        success=True,
        message="File deleted successfully.",
        data={"path": str(path)},
    )


@router.post("/mkdir", response_model=ToolResponse)
def create_directory(request: CreateDirectoryRequest):

    path = service.create_directory(request.path)

    return ToolResponse(
        success=True,
        message="Directory created successfully.",
        data={"path": str(path)},
    )


@router.post("/list", response_model=ToolResponse)
def list_directory(request: ListDirectoryRequest):
    items = service.list_directory(request.path)

    return ToolResponse(
        success=True,
        message="Directory listed successfully.",
        data={"items": items},
    )


@router.post("/exists", response_model=ToolResponse)
def exists(request: ExistsRequest):
    return ToolResponse(
        success=True,
        message="Path check completed.",
        data={"exists": service.exists(request.path)},
    )
