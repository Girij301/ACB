from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ExecutionHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    session_id: str
    plan_id: int

    status: str

    started_at: datetime
    completed_at: datetime | None

    duration_ms: int

    total_steps: int
    successful_steps: int
    failed_steps: int

    retry_count: int
    debug_count: int
    validation_count: int

    created_at: datetime
    updated_at: datetime


class ExecutionStepResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    execution_id: int

    step_index: int

    action: str
    description: str

    status: str

    tool_name: str | None

    output: str | None
    error: str | None

    duration_ms: int

    started_at: datetime
    completed_at: datetime | None

    created_at: datetime


class ValidationRecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    execution_id: int

    validator_name: str

    passed: bool

    stdout: str | None
    stderr: str | None

    duration_ms: int

    created_at: datetime


class RetryRecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    execution_id: int

    step_index: int
    attempt_number: int

    reason: str
    previous_error: str | None

    success: bool

    created_at: datetime


class DebugRecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    execution_id: int

    step_index: int
    attempt_number: int

    failure_summary: str
    ai_summary: str | None

    success: bool

    created_at: datetime
