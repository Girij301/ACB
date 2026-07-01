from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class PlannerRequest(BaseModel):
    session_id: str = Field(
        ...,
        min_length=1,
        description="Unique conversation session ID",
    )

    task: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="Task to generate an execution plan for",
    )


class ActionType(str, Enum):
    CREATE_DIRECTORY = "create_directory"
    CREATE_FILE = "create_file"
    WRITE_FILE = "write_file"
    APPEND_FILE = "append_file"
    DELETE_FILE = "delete_file"
    READ_FILE = "read_file"
    LIST_DIRECTORY = "list_directory"
    RUN_TERMINAL = "run_terminal"


class PlanStep(BaseModel):
    step: int = Field(
        ...,
        gt=0,
        description="Sequential step number",
    )

    action: ActionType = Field(
        ...,
        description="Action to be executed by the execution engine",
    )

    description: str = Field(
        ...,
        min_length=1,
        description="Human-readable description of the step",
    )

    parameters: dict[str, Any] = Field(
        default_factory=dict,
        description="Arguments required for the action",
    )


class PlannerResponse(BaseModel):
    task: str

    plan: list[PlanStep]
