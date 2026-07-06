from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ActionType(str, Enum):
    CREATE_DIRECTORY = "create_directory"
    CREATE_FILE = "create_file"
    WRITE_FILE = "write_file"
    APPEND_FILE = "append_file"
    DELETE_FILE = "delete_file"
    READ_FILE = "read_file"
    LIST_DIRECTORY = "list_directory"
    RUN_TERMINAL = "run_terminal"


class PlannerRequest(BaseModel):
    session_id: str = Field(...)

    task: str = Field(...)


class PlanStep(BaseModel):
    step: int

    action: ActionType

    description: str

    goal: str | None = None

    parameters: dict[str, Any] = Field(default_factory=dict)


class PlannerResponse(BaseModel):
    task: str

    plan: list[PlanStep]