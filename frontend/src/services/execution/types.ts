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

export interface ExecutionInfo {
  container_id?: string;
  workspace?: string;
}

export interface ExecutionResponse {
  success: boolean;

  steps: StepResult[];

  execution_info?: ExecutionInfo | null;
}