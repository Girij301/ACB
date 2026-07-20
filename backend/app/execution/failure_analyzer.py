from app.schemas.execution import StepResult
from app.schemas.failure import FailureAnalysis, FailureCategory
from app.schemas.planner import ActionType
from app.schemas.validation import ValidationResult


class FailureAnalyzer:
    """
    Classifies execution and validation failures.
    """

    def analyze(
        self,
        result: StepResult | ValidationResult,
    ) -> FailureAnalysis:
        """
        Analyze execution or validation failures.
        """

        if isinstance(result, ValidationResult):
            return self._analyze_validation(result)

        return self._analyze_execution(result)

    def _analyze_execution(
        self,
        result: StepResult,
    ) -> FailureAnalysis:
        """
        Analyze execution failures.
        """

        output = result.output or {}

        error_type = output.get("error_type")
        action = output.get("action")

        # Filesystem failures
        if error_type in {
            "FileNotFoundError",
            "FileExistsError",
            "PermissionError",
            "IsADirectoryError",
            "NotADirectoryError",
        }:
            return FailureAnalysis(
                category=FailureCategory.FILESYSTEM,
                retryable=False,
                reason=output.get(
                    "error",
                    "Filesystem error.",
                ),
            )
        
        # Terminal failures
        if action == ActionType.RUN_TERMINAL.value:
            exit_code = output.get("exit_code", -1)

            stderr = output.get("stderr", "") or ""
            error = output.get("error", "") or ""

            combined_output = f"{stderr}\n{error}".lower()

            # Interactive CLI program
            if (
                "eoferror: eof when reading a line" in combined_output
                or "input(" in combined_output
                or "requires interactive" in combined_output
            ):
                return FailureAnalysis(
                    category=FailureCategory.TERMINAL,
                    retryable=False,
                    reason=(
                        "Program requires interactive terminal input "
                        "and cannot be executed automatically."
                    ),
                )

            # Missing command-line arguments
            if (
                "usage:" in combined_output
                or "missing required arguments" in combined_output
                or "the following arguments are required" in combined_output
            ):
                return FailureAnalysis(
                    category=FailureCategory.TERMINAL,
                    retryable=False,
                    reason=(
                        "The command requires additional input or "
                        "command-line arguments."
                    ),
                )

            return FailureAnalysis(
                category=FailureCategory.TERMINAL,
                retryable=exit_code != 0,
                reason=(stderr or error or "Terminal error."),
            )

        # Unknown failures
        return FailureAnalysis(
            category=FailureCategory.UNKNOWN,
            retryable=False,
            reason=output.get(
                "error",
                "Unknown failure.",
            ),
        )

    def _analyze_validation(
        self,
        result: ValidationResult,
    ) -> FailureAnalysis:
        """
        Analyze validation failures.
        """

        return FailureAnalysis(
            category=FailureCategory.VALIDATION,
            retryable=True,
            reason=result.message or f"{result.validator} failed.",
        )
