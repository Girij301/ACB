from app.schemas.validation import ValidationResult


def test_validation_result_creation():
    """
    ValidationResult should be created with all fields.
    """

    result = ValidationResult(
        success=True,
        validator="ruff",
        output={"files_checked": 10},
        message="Validation passed.",
    )

    assert result.success is True
    assert result.validator == "ruff"
    assert result.output == {"files_checked": 10}
    assert result.message == "Validation passed."


def test_validation_result_optional_fields():
    """
    Optional fields should default to None.
    """

    result = ValidationResult(
        success=False,
        validator="pytest",
    )

    assert result.success is False
    assert result.validator == "pytest"
    assert result.output is None
    assert result.message is None


def test_validation_result_model_dump():
    """
    ValidationResult should serialize correctly.
    """

    result = ValidationResult(
        success=True,
        validator="ruff",
        output={"checked": 5},
        message="OK",
    )

    dumped = result.model_dump()

    assert dumped == {
        "success": True,
        "validator": "ruff",
        "output": {"checked": 5},
        "message": "OK",
    }
