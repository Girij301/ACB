from pydantic import BaseModel

from app.schemas.validation import ValidationResult


class ValidationExecutionResult(BaseModel):
    """
    Represents the outcome of the validation workflow.
    """

    success: bool
    attempts: int = 1
    results: list[ValidationResult]
