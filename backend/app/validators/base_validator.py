from abc import ABC, abstractmethod

from app.execution.context import ExecutionContext
from app.schemas.validation import ValidationResult


class BaseValidator(ABC):
    """
    Base class for all validators.
    """

    @abstractmethod
    def validate(
        self,
        context: ExecutionContext,
    ) -> ValidationResult:
        pass
