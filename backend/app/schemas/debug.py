from pydantic import BaseModel, Field


class FilePatch(BaseModel):
    """
    Represents a modification to a single file.
    """

    path: str
    content: str


class DebugSuggestion(BaseModel):
    """
    AI-generated debugging suggestion.
    """

    summary: str
    explanation: str

    files: list[FilePatch] = Field(default_factory=list)

    commands: list[str] = Field(default_factory=list)
