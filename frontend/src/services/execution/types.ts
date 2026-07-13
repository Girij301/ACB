export interface ExecuteRequest {
  session_id: string;
  task: string;
}

export type ExecutionStatus = "success" | "failed" | "pending";

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
  completed_at: string | null;
}

export interface ExecutionStartResponse {
  success: boolean;
  status: string;
  message: string;
  session_id: string;
}

export type ExecutionEventType =
  | "execution_started"
  | "execution_finished"
  | "step_started"
  | "step_completed"
  | "retry_started"
  | "retry_completed"
  | "debug_started"
  | "debug_completed"
  | "validation_started"
  | "validation_completed";

export interface ExecutionEvent {
  type: ExecutionEventType;
  timestamp: string;
  session_id: string | null;
  execution_id: number | null;
  step_number: number | null;
  message: string;
  payload: Record<string, unknown> | null;
}
