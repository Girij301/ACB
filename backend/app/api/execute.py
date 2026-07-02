from app.core.database import get_db
from app.schemas.execute import ExecuteRequest
from app.services.agent_service import AgentService
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/execute")
def execute(
    request: ExecuteRequest,
    db: Session = Depends(get_db),
):
    agent_service = AgentService(db=db)
    return agent_service.execute(request)
