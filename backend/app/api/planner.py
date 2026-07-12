from app.core.logger import logger
from app.schemas.base import APIResponse
from app.schemas.planner import PlannerRequest
from app.services.plan_memory import save_plan
from app.services.planner_service import PlannerService
from fastapi import APIRouter

router = APIRouter()

planner_service = PlannerService()


@router.post("/planner", response_model=APIResponse)
def create_plan(request: PlannerRequest):

    logger.info(f"Planner request | Session={request.session_id}")

    plan = planner_service.create_plan(request.task)

    save_plan(
        session_id=request.session_id,
        user_task=request.task,
        plan=plan.model_dump(),
    )

    logger.info("Planner request completed successfully.")

    return APIResponse(
        message="Execution plan generated successfully.",
        data=plan,
    )
