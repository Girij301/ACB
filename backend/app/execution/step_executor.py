from app.execution.context import ExecutionContext
from app.execution.tool_registry import ToolRegistry
from app.schemas.execution import ExecutionStatus, StepResult
from app.schemas.planner import ActionType, PlanStep
from app.tools.terminal_tool import TerminalTool


class StepExecutor:
    """
    Executes a single step of an execution plan.

    This class is responsible for dispatching a plan step
    to the appropriate tool.
    """

    def __init__(
        self,
        terminal_tool: TerminalTool | None = None,
    ) -> None:
        self.terminal_tool = terminal_tool or TerminalTool()

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
                terminal_tool=self.terminal_tool,
            )

            handler = registry.get_handler(step)

            if handler is None:
                raise NotImplementedError(f"Unsupported action: {step.action}")

            tool_output = handler()

            # Terminal commands may fail without raising exceptions.
            if step.action == ActionType.RUN_TERMINAL and not tool_output.get(
                "success", False
            ):
                return StepResult(
                    step_number=step.step,
                    description=step.description,
                    status=ExecutionStatus.FAILED,
                    message="Terminal command failed.",
                    output={
                        **tool_output,
                        "action": step.action.value,
                    },
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
