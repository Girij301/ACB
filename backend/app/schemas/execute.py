from pydantic import BaseModel, Field


class ExecuteRequest(BaseModel):
    """
    Request for the complete AI execution pipeline.
    """

    session_id: str = Field(
        ...,
        min_length=1,
    )

    task: str = Field(
        ...,
        min_length=3,
        max_length=1000,
    )