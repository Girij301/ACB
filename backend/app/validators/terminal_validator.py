from app.execution.context import ExecutionContext
from app.schemas.validation import ValidationResult
from app.tools.terminal_tool import TerminalTool
from app.validators.base_validator import BaseValidator


class TerminalValidator(BaseValidator):
    """
    Executes a terminal command to validate the workspace.
    """

    def __init__(
        self,
        command: str,
        terminal_tool: TerminalTool | None = None,
    ) -> None:
        self.command = command
        self.terminal_tool = terminal_tool or TerminalTool()

    def validate(
        self,
        context: ExecutionContext,
    ) -> ValidationResult:
        """
        Execute the validation command.
        """

        result = self.terminal_tool.run(
            command=self.command,
            cwd=".",
        )

        return ValidationResult(
            success=result["success"],
            validator=self.command,
            output=result,
            message=(
                "Validation passed." if result["success"] else "Validation failed."
            ),
        )
