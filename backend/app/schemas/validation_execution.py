from app.schemas.validation import ValidationResult
from pydantic import BaseModel


class ValidationExecutionResult(BaseModel):
    """
    Represents the outcome of the validation workflow.
    """

    success: bool
    attempts: int = 1
    results: list[ValidationResult]
