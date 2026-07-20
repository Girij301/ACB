from datetime import datetime
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


class ExecutionSummary(BaseModel):
    execution_id: int
    session_id: str
    plan_id: int
    status: str
    workspace: str
    total_steps: int
    successful_steps: int
    failed_steps: int
    retry_count: int
    debug_count: int
    validation_count: int
    duration_ms: int
    started_at: datetime
    completed_at: datetime | None = None


class ExecutionResult(BaseModel):
    success: bool

    steps: list[StepResult]

    execution: ExecutionSummary | None = None
