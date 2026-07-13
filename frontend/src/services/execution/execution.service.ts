import { api } from "@/services/api";

import type { ExecuteRequest, ExecutionStartResponse } from "./types";

export class ExecutionService {
  static async execute(
    payload: ExecuteRequest,
  ): Promise<ExecutionStartResponse> {
    const { data } = await api.post<ExecutionStartResponse>(
      "/execute",
      payload,
    );

    return data;
  }
}
