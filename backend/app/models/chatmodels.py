from app.models.base import APIResponse
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: str = Field(..., description="Unique conversation session ID")
    message: str = Field(..., min_length=1, max_length=2000)


class ChatResponse(APIResponse):
    pass
