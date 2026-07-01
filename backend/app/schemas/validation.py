from pydantic import BaseModel


class ValidationResult(BaseModel):
    success: bool
    validator: str
    output: dict | None = None
    message: str | None = None
