from fastapi import APIRouter

from app.schemas.common import ToolResponse
from app.schemas.terminal import TerminalRequest
from app.services.terminal_service import TerminalService

router = APIRouter(prefix="/terminal", tags=["Terminal"])

service = TerminalService()


@router.post("/run", response_model=ToolResponse)
def run_command(request: TerminalRequest):

    result = service.execute_command(
        command=request.command,
        cwd=request.cwd,
        timeout=request.timeout,
    )

    return ToolResponse(
        success=result["success"],
        message=(
            "Command executed successfully."
            if result["success"]
            else "Command execution failed."
        ),
        data=result,
    )
