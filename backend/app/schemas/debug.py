from pydantic import BaseModel, Field


class FilePatch(BaseModel):
    """
    Represents a modification to a single file.
    """

    path: str
    content: str


class CommandPatch(BaseModel):
    """
    Represents a replacement for a failed terminal command.
    """

    old: str
    new: str


class DependencyPatch(BaseModel):
    """
    Represents a dependency that must be installed
    before retrying the failed command.
    """

    package: str
    manager: str = "pip"


class DebugSuggestion(BaseModel):
    """
    AI-generated debugging suggestion.
    """

    summary: str
    explanation: str

    files: list[FilePatch] = Field(default_factory=list)

    commands: list[CommandPatch] = Field(default_factory=list)

    dependencies: list[DependencyPatch] = Field(default_factory=list)