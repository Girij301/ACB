from enum import Enum

from pydantic import BaseModel


class ExecutionStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"


class StepResult(BaseModel):
    step_number: int
    description: str
    status: ExecutionStatus
    message: str | None = None
    output: dict | None = None


class ExecutionResult(BaseModel):
    success: bool
    steps: list[StepResult]
