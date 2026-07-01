from app.schemas.validation import ValidationResult
from app.validators.base_validator import BaseValidator
from app.validators.validation_manager import ValidationManager


class SuccessValidator(BaseValidator):
    def validate(self, context):
        return ValidationResult(
            success=True,
            validator="success",
            message="Passed",
        )


class FailureValidator(BaseValidator):
    def validate(self, context):
        return ValidationResult(
            success=False,
            validator="failure",
            message="Failed",
        )


def test_validation_manager_starts_empty():
    """
    ValidationManager should start without validators
    when an empty list is provided.
    """
    manager = ValidationManager(validators=[])

    assert manager.validators == []
    assert manager.has_validators() is False


def test_add_validator():
    """
    Validators should be added successfully.
    """
    manager = ValidationManager(validators=[])

    validator = SuccessValidator()

    manager.add_validator(validator)

    assert manager.has_validators() is True
    assert len(manager.validators) == 1
    assert manager.validators[0] is validator


def test_clear_validators():
    """
    clear() should remove every registered validator.
    """
    manager = ValidationManager(
        validators=[
            SuccessValidator(),
            FailureValidator(),
        ]
    )

    assert manager.has_validators() is True

    manager.clear()

    assert manager.validators == []
    assert manager.has_validators() is False


def test_validate_returns_all_results():
    """
    validate() should execute every validator.
    """
    manager = ValidationManager(
        validators=[
            SuccessValidator(),
            FailureValidator(),
        ]
    )

    results = manager.validate(None)

    assert len(results) == 2

    assert results[0].success is True
    assert results[1].success is False


def test_all_passed_returns_true():
    """
    all_passed() should return True when every
    validator succeeds.
    """
    manager = ValidationManager(
        validators=[
            SuccessValidator(),
            SuccessValidator(),
        ]
    )

    success, results = manager.all_passed(None)

    assert success is True
    assert len(results) == 2


def test_all_passed_returns_false():
    """
    all_passed() should return False when any
    validator fails.
    """
    manager = ValidationManager(
        validators=[
            SuccessValidator(),
            FailureValidator(),
        ]
    )

    success, results = manager.all_passed(None)

    assert success is False
    assert len(results) == 2


def test_has_validators():
    """
    has_validators() should reflect the current state.
    """
    manager = ValidationManager(validators=[])

    assert manager.has_validators() is False

    manager.add_validator(SuccessValidator())

    assert manager.has_validators() is True
