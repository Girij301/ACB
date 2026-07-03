from app.execution.context import ExecutionContext
from app.execution.tool_registry import ToolRegistry
from app.schemas.execution import ExecutionStatus, StepResult
from app.schemas.planner import ActionType, PlanStep
from app.services.docker_terminal_service import DockerTerminalService


class StepExecutor:
    """
    Executes a single step of an execution plan.

    This class is responsible for dispatching a plan step
    to the appropriate tool.
    """

    def __init__(
        self,
        terminal_service: DockerTerminalService | None = None,
    ) -> None:
        self.terminal_service = terminal_service or DockerTerminalService()

    def execute(
        self,
        step: PlanStep,
        context: ExecutionContext,
    ) -> StepResult:
        """
        Execute a single plan step.
        """

        try:
            registry = ToolRegistry(
                context=context,
                terminal_service=self.terminal_service,
            )

            handler = registry.get_handler(step)

            if handler is None:
                raise NotImplementedError(f"Unsupported action: {step.action}")

            tool_output = handler()

            # Terminal commands may fail without raising exceptions.
            if step.action == ActionType.RUN_TERMINAL:

                # -----------------------------
                # Docker execution result object
                # -----------------------------
                if hasattr(tool_output, "success"):

                    if not tool_output.success:
                        return StepResult(
                            step_number=step.step,
                            description=step.description,
                            status=ExecutionStatus.FAILED,
                            message="Terminal command failed.",
                            output={
                                "stdout": tool_output.stdout,
                                "stderr": tool_output.stderr,
                                "exit_code": tool_output.exit_code,
                                "execution_time": tool_output.execution_time,
                                "timed_out": (
                                    tool_output.execution_info.timed_out
                                    if getattr(
                                        tool_output,
                                        "execution_info",
                                        None,
                                    )
                                    else False
                                ),
                                "action": step.action.value,
                            },
                        )

                    return StepResult(
                        step_number=step.step,
                        description=step.description,
                        status=ExecutionStatus.SUCCESS,
                        message="Step executed successfully.",
                        output={
                            "success": True,
                            "stdout": tool_output.stdout,
                            "stderr": tool_output.stderr,
                            "exit_code": tool_output.exit_code,
                            "execution_time": tool_output.execution_time,
                        },
                    )

                # -----------------------------
                # Local executor dictionary
                # -----------------------------
                if isinstance(tool_output, dict):

                    return StepResult(
                        step_number=step.step,
                        description=step.description,
                        status=(
                            ExecutionStatus.SUCCESS
                            if tool_output["success"]
                            else ExecutionStatus.FAILED
                        ),
                        message=(
                            "Step executed successfully."
                            if tool_output["success"]
                            else "Terminal command failed."
                        ),
                        output=tool_output,
                    )

            if isinstance(tool_output, dict):
                output = tool_output

            elif tool_output is None:
                output = None

            else:
                output = {
                    "result": str(tool_output),
                }

            return StepResult(
                step_number=step.step,
                description=step.description,
                status=ExecutionStatus.SUCCESS,
                message="Step executed successfully.",
                output=output,
            )

        except Exception as exc:
            return StepResult(
                step_number=step.step,
                description=step.description,
                status=ExecutionStatus.FAILED,
                message="Step execution failed.",
                output={
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                    "action": step.action.value,
                    "parameters": step.parameters,
                },
            )
