from app.execution.validation_engine import ValidationEngine
from app.schemas.validation import ValidationResult
from app.validators.validation_manager import ValidationManager


class SuccessValidationManager(ValidationManager):
    def __init__(self):
        pass

    def all_passed(self, context):
        return (
            True,
            [
                ValidationResult(
                    success=True,
                    validator="ruff",
                    message="Validation passed.",
                )
            ],
        )


class FailureValidationManager(ValidationManager):
    def __init__(self):
        pass

    def all_passed(self, context):
        return (
            False,
            [
                ValidationResult(
                    success=False,
                    validator="compileall",
                    message="Validation failed.",
                )
            ],
        )


def test_validation_engine_success():
    """
    ValidationEngine should return a successful
    ValidationExecutionResult when validation passes.
    """

    engine = ValidationEngine(validation_manager=SuccessValidationManager())

    result = engine.validate(
        context=None,
        history=[],
    )

    assert result.success is True
    assert result.attempts == 1
    assert len(result.results) == 1

    validation = result.results[0]

    assert validation.success is True
    assert validation.validator == "ruff"


def test_validation_engine_failure():
    """
    ValidationEngine should return a failed
    ValidationExecutionResult when validation fails.
    """

    engine = ValidationEngine(validation_manager=FailureValidationManager())

    result = engine.validate(
        context=None,
        history=[],
    )

    assert result.success is False
    assert result.attempts == 1
    assert len(result.results) == 1

    validation = result.results[0]

    assert validation.success is False
    assert validation.validator == "compileall"
