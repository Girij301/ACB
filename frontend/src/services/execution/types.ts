export interface ExecuteRequest {
  session_id: string;
  task: string;
}

export type ExecutionStatus =
  | "success"
  | "failed"
  | "pending";

export interface StepResult {
  step_number: number;
  description: string;
  status: ExecutionStatus;
  message?: string | null;
  output?: Record<string, unknown> | null;
}

export interface ExecutionSummary {
  execution_id: number;
  session_id: string;
  plan_id: number;

  status: string;

  workspace: string;

  total_steps: number;
  successful_steps: number;
  failed_steps: number;

  retry_count: number;
  debug_count: number;
  validation_count: number;

  duration_ms: number;

  started_at: string;
  completed_at: string;
}

export interface ExecutionResponse {
  success: boolean;

  steps: StepResult[];

  execution: ExecutionSummary;
}