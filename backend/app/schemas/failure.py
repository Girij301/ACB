from enum import Enum

from pydantic import BaseModel


class FailureCategory(str, Enum):
    FILESYSTEM = "filesystem"
    TERMINAL = "terminal"
    VALIDATION = "validation"
    UNKNOWN = "unknown"


class FailureAnalysis(BaseModel):
    category: FailureCategory
    retryable: bool
    reason: str
