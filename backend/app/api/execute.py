from app.schemas.execute import ExecuteRequest
from app.services.agent_service import AgentService
from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.database import get_db

router = APIRouter()

@router.post("/execute")
def execute(
    request: ExecuteRequest,
    db: Session = Depends(get_db),
):
    agent_service = AgentService(db=db)
    return agent_service.execute(request)