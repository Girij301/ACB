import type { ExecutionEvent, ExecutionSummary, StepResult } from "./types";

export interface ExecutionState {
  loading: boolean;

  connected: boolean;

  error: string | null;

  execution: ExecutionSummary | null;

  steps: StepResult[];

  events: ExecutionEvent[];

  activeStep: number | null;

  retryingStep: number | null;

  debuggingStep: number | null;

  validating: boolean;

  totalSteps: number;

  completedSteps: number;

  successfulSteps: number;

  failedSteps: number;

  progress: number;
}

export const initialExecutionState: ExecutionState = {
  loading: false,
  connected: false,
  error: null,
  execution: null,
  steps: [],
  events: [],
  activeStep: null,
  retryingStep: null,
  debuggingStep: null,
  validating: false,
  totalSteps: 0,
  completedSteps: 0,
  successfulSteps: 0,
  failedSteps: 0,
  progress: 0,
};

function calculateProgress(completed: number, total: number): number {
  if (total === 0) {
    return 0;
  }

  return Math.round((completed / total) * 100);
}

export function executionReducer(
  state: ExecutionState,
  event: ExecutionEvent,
): ExecutionState {
  const nextState: ExecutionState = {
    ...state,
    events: [...state.events, event],
  };

  switch (event.type) {
    case "execution_started":
      return {
        ...nextState,
        loading: true,
        error: null,
        totalSteps: Number(event.payload?.total_steps) || 0,
        completedSteps: 0,
        successfulSteps: 0,
        failedSteps: 0,
        progress: 0,
      };

    case "execution_finished":
      return {
        ...nextState,
        loading: false,
        activeStep: null,
        retryingStep: null,
        debuggingStep: null,
        validating: false,
        progress: 100,
      };

    case "step_started": {
      if (event.step_number === null) {
        return nextState;
      }

      const exists = nextState.steps.some(
        (step) => step.step_number === event.step_number,
      );

      if (exists) {
        return {
          ...nextState,
          activeStep: event.step_number,
        };
      }

      return {
        ...nextState,
        activeStep: event.step_number,
        steps: [
          ...nextState.steps,
          {
            step_number: event.step_number,
            description: event.message,
            status: "pending",
            message: null,
            output: null,
          },
        ],
      };
    }

    case "step_completed": {
      if (event.step_number === null) {
        return nextState;
      }

      const status = event.payload?.status === "success" ? "success" : "failed";

      const completed = nextState.completedSteps + 1;

      const successful =
        status === "success"
          ? nextState.successfulSteps + 1
          : nextState.successfulSteps;

      const failed =
        status === "failed" ? nextState.failedSteps + 1 : nextState.failedSteps;

      return {
        ...nextState,

        activeStep: null,

        completedSteps: completed,

        successfulSteps: successful,

        failedSteps: failed,

        progress: calculateProgress(completed, nextState.totalSteps),

        steps: nextState.steps.map((step) =>
          step.step_number === event.step_number
            ? {
                ...step,
                status,
                message: event.message,
                output:
                  (event.payload?.output as
                    | Record<string, unknown>
                    | null
                    | undefined) ?? null,
              }
            : step,
        ),
      };
    }

    case "retry_started":
      return {
        ...nextState,
        retryingStep: event.step_number,
      };

    case "retry_completed":
      return {
        ...nextState,
        retryingStep: null,
      };

    case "debug_started":
      return {
        ...nextState,
        debuggingStep: event.step_number,
      };

    case "debug_completed":
      return {
        ...nextState,
        debuggingStep: null,
      };

    case "validation_started":
      return {
        ...nextState,
        validating: true,
      };

    case "validation_completed":
      return {
        ...nextState,
        validating: false,
      };

    default:
      return nextState;
  }
}
