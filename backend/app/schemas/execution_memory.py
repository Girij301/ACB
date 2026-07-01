from app.schemas.execution import StepResult
from pydantic import BaseModel, Field


class ExecutionMemory(BaseModel):
    """
    Stores execution history during a plan run.
    """

    step_results: list[StepResult] = Field(default_factory=list)

    # Terminal retry counter
    retry_count: int = 0

    # AI debugging / patch attempts
    ai_fix_attempts: int = 0

    def add_result(
        self,
        result: StepResult,
    ) -> None:
        self.step_results.append(result)

    def increment_retry(self) -> None:
        """
        Increment the terminal retry counter.
        """
        self.retry_count += 1

    def reset_retry(self) -> None:
        """
        Reset the terminal retry counter before
        executing a new step.
        """
        self.retry_count = 0

    def increment_ai_fix_attempt(self) -> None:
        """
        Increment the AI fix attempt counter.
        """
        self.ai_fix_attempts += 1

    def reset_ai_fix_attempts(self) -> None:
        """
        Reset the AI fix attempt counter before
        executing a new step.
        """
        self.ai_fix_attempts = 0

    @property
    def failed_steps(self) -> list[StepResult]:
        return [step for step in self.step_results if step.status.value == "failed"]

    @property
    def successful_steps(self) -> list[StepResult]:
        return [step for step in self.step_results if step.status.value == "success"]
