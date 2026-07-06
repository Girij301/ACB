import { api } from "@/services/api";

import type {
  ExecuteRequest,
  ExecutionResponse,
} from "./types";

export class ExecutionService {
  static async execute(
    payload: ExecuteRequest,
  ): Promise<ExecutionResponse> {
    const { data } =
      await api.post<ExecutionResponse>(
        "/execute",
        payload,
      );

    return data;
  }
}