export interface PlannerRequest {
  session_id: string;
  task: string;
}

export type ActionType =
  | "create_directory"
  | "create_file"
  | "write_file"
  | "append_file"
  | "delete_file"
  | "read_file"
  | "list_directory"
  | "run_terminal";

export interface PlanStep {
  step: number;
  action: ActionType;
  description: string;
  parameters: Record<string, unknown>;
}

export interface PlannerData {
  task: string;
  plan: PlanStep[];
}

export interface PlannerResponse {
  success: boolean;
  message: string;
  data: PlannerData;
  error: string | null;
}