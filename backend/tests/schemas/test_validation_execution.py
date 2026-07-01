from app.schemas.validation import ValidationResult
from app.schemas.validation_execution import ValidationExecutionResult


def test_validation_execution_result_success():
    """
    ValidationExecutionResult should store
    a successful validation outcome.
    """
    result = ValidationExecutionResult(
        success=True,
        results=[
            ValidationResult(
                success=True,
                validator="ruff",
                message="Passed",
            )
        ],
    )

    assert result.success is True
    assert result.attempts == 1
    assert len(result.results) == 1
    assert result.results[0].validator == "ruff"


def test_validation_execution_result_failed():
    """
    ValidationExecutionResult should store
    a failed validation outcome.
    """
    result = ValidationExecutionResult(
        success=False,
        attempts=2,
        results=[
            ValidationResult(
                success=False,
                validator="compileall",
                message="Failed",
            )
        ],
    )

    assert result.success is False
    assert result.attempts == 2
    assert len(result.results) == 1
    assert result.results[0].success is False


def test_validation_execution_result_empty_results():
    """
    ValidationExecutionResult should allow
    an empty validation result list.
    """
    result = ValidationExecutionResult(
        success=True,
        results=[],
    )

    assert result.success is True
    assert result.attempts == 1
    assert result.results == []
