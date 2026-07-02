from app.schemas.execute import ExecuteRequest
from app.schemas.execution import ExecutionResult
from app.services.agent_service import AgentService
from fastapi import APIRouter

router = APIRouter()

agent_service = AgentService()


@router.post(
    "/execute",
    response_model=ExecutionResult,
    tags=["Execution"],
)
def execute(
    request: ExecuteRequest,
) -> ExecutionResult:
    """
    Generate a plan using Gemini and execute it.
    """
    return agent_service.execute(request)
