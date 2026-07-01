import pytest
from app.execution.context import ExecutionContext
from app.schemas.validation import ValidationResult
from app.validators.base_validator import BaseValidator


def test_base_validator_cannot_be_instantiated():
    """
    BaseValidator is abstract and cannot be instantiated.
    """

    with pytest.raises(TypeError):
        BaseValidator()


class DummyValidator(BaseValidator):
    """
    Simple concrete validator for testing.
    """

    def validate(
        self,
        context: ExecutionContext,
    ) -> ValidationResult:
        return ValidationResult(
            success=True,
            validator="dummy",
        )


def test_dummy_validator_is_instance_of_base_validator():
    """
    A concrete validator should inherit from BaseValidator.
    """

    validator = DummyValidator()

    assert isinstance(
        validator,
        BaseValidator,
    )


def test_dummy_validator_validate():
    """
    Concrete validators should return ValidationResult.
    """

    validator = DummyValidator()

    result = validator.validate(None)

    assert isinstance(
        result,
        ValidationResult,
    )

    assert result.success is True
    assert result.validator == "dummy"
