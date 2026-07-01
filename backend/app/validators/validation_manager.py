from app.core.config import settings
from app.core.logger import logger
from app.execution.context import ExecutionContext
from app.schemas.validation import ValidationResult
from app.validators.base_validator import BaseValidator
from app.validators.terminal_validator import TerminalValidator


class ValidationManager:
    """
    Manages and executes all registered validators.
    """

    def __init__(
        self,
        validators: list[BaseValidator] | None = None,
    ) -> None:
        print("validators =", validators)

        if validators is None:
            self.validators: list[BaseValidator] = []

            if settings.ENABLE_VALIDATION:
                print("Registering defaults")
                self._register_default_validators()
        else:
            self.validators = validators

    def _register_default_validators(self) -> None:
        """
        Register validators defined in the application
        configuration.
        """

        for command in settings.DEFAULT_VALIDATORS:
            self.add_validator(TerminalValidator(command))

    def add_validator(
        self,
        validator: BaseValidator,
    ) -> None:
        """
        Register a new validator.
        """
        self.validators.append(validator)

    def validate(
        self,
        context: ExecutionContext,
    ) -> list[ValidationResult]:
        """
        Execute every registered validator.
        """

        results: list[ValidationResult] = []

        for validator in self.validators:

            result = validator.validate(context)

            logger.info(
                "Validation | " f"{result.validator} | " f"Success={result.success}"
            )

            results.append(result)

        return results

    def all_passed(
        self,
        context: ExecutionContext,
    ) -> tuple[bool, list[ValidationResult]]:
        """
        Execute all validators and return whether
        every validation passed.
        """

        results = self.validate(context)

        success = all(result.success for result in results)

        return success, results

    def has_validators(self) -> bool:
        """
        Return True if validators are registered.
        """

        return bool(self.validators)

    def clear(self) -> None:
        """
        Remove all registered validators.
        """

        self.validators.clear()
