from pydantic import BaseModel, Field

from app.schemas.base import APIResponse


class ChatRequest(BaseModel):
    session_id: str = Field(
        ...,
        description="Unique conversation session ID",
    )

    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
    )


class ChatResponse(APIResponse):
    pass
