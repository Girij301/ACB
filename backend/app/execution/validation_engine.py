from app.execution.context import ExecutionContext
from app.schemas.validation_execution import ValidationExecutionResult
from app.validators.validation_manager import ValidationManager


class ValidationEngine:
    """
    Coordinates the validation workflow.
    """

    def __init__(
        self,
        validation_manager: ValidationManager | None = None,
    ) -> None:
        self.validation_manager = validation_manager or ValidationManager()

    def validate(
        self,
        context: ExecutionContext,
        history: list,
    ) -> ValidationExecutionResult:
        """
        Execute all registered validators.
        """

        success, results = self.validation_manager.all_passed(context)

        return ValidationExecutionResult(
            success=success,
            attempts=1,
            results=results,
        )
