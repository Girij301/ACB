from unittest.mock import Mock

from app.schemas.validation import ValidationResult
from app.validators.terminal_validator import TerminalValidator


def test_terminal_validator_success():
    """
    TerminalValidator should return a successful
    ValidationResult when the command succeeds.
    """

    terminal_tool = Mock()

    terminal_tool.run.return_value = {
        "success": True,
        "stdout": "All checks passed.",
        "stderr": "",
        "returncode": 0,
    }

    validator = TerminalValidator(
        command="ruff check .",
        terminal_tool=terminal_tool,
    )

    result = validator.validate(None)

    terminal_tool.run.assert_called_once_with(
        command="ruff check .",
        cwd=".",
    )

    assert isinstance(result, ValidationResult)
    assert result.success is True
    assert result.validator == "ruff check ."
    assert result.message == "Validation passed."
    assert result.output["returncode"] == 0


def test_terminal_validator_failure():
    """
    TerminalValidator should return a failed
    ValidationResult when the command fails.
    """

    terminal_tool = Mock()

    terminal_tool.run.return_value = {
        "success": False,
        "stdout": "",
        "stderr": "Found lint errors.",
        "returncode": 1,
    }

    validator = TerminalValidator(
        command="ruff check .",
        terminal_tool=terminal_tool,
    )

    result = validator.validate(None)

    terminal_tool.run.assert_called_once_with(
        command="ruff check .",
        cwd=".",
    )

    assert isinstance(result, ValidationResult)
    assert result.success is False
    assert result.validator == "ruff check ."
    assert result.message == "Validation failed."
    assert result.output["stderr"] == "Found lint errors."


def test_terminal_validator_preserves_output():
    """
    TerminalValidator should preserve the complete
    terminal output inside ValidationResult.
    """

    terminal_output = {
        "success": True,
        "stdout": "Everything OK",
        "stderr": "",
        "returncode": 0,
        "execution_time": 0.42,
    }

    terminal_tool = Mock()
    terminal_tool.run.return_value = terminal_output

    validator = TerminalValidator(
        command="pytest",
        terminal_tool=terminal_tool,
    )

    result = validator.validate(None)

    assert result.output == terminal_output
