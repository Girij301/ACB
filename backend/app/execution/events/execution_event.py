from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.execution.events.event_types import ExecutionEventType


class ExecutionEvent(BaseModel):
    """
    Represents a single execution event.
    """

    type: ExecutionEventType
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    session_id: str | None = None
    execution_id: int | None = None
    step_number: int | None = None
    message: str
    payload: dict[str, Any] | None = None
