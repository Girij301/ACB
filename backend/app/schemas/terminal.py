from pydantic import BaseModel, Field


class TerminalRequest(BaseModel):
    command: str = Field(..., description="Command to execute")
    cwd: str = Field(default=".", description="Working directory inside the workspace")
    timeout: int = Field(
        default=60, ge=1, le=300, description="Maximum execution time in seconds"
    )


class TerminalResponse(BaseModel):
    success: bool = Field(..., description="Whether the command executed successfully")
    command: str = Field(..., description="Executed command")
    cwd: str = Field(..., description="Working directory used for execution")
    stdout: str = Field(default="", description="Standard output from the command")
    stderr: str = Field(
        default="", description="Standard error output from the command"
    )
    exit_code: int = Field(..., description="Process exit code")
    execution_time: float = Field(..., description="Execution time in seconds")
