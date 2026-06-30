from typing import List

from pydantic import BaseModel, Field


class PlannerRequest(BaseModel):
    session_id: str = Field(
        ..., min_length=1, description="Unique conversation session ID"
    )

    task: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="Task to generate an execution plan for",
    )


class PlanStep(BaseModel):
    step: int = Field(..., gt=0)
    description: str = Field(..., min_length=1)


class PlannerResponse(BaseModel):
    task: str
    plan: List[PlanStep]
