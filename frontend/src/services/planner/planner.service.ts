import { api } from "@/services/api";

import type {
  PlannerRequest,
  PlannerResponse,
} from "./types";

export class PlannerService {
  static async createPlan(
    payload: PlannerRequest,
  ): Promise<PlannerResponse> {
    const { data } =
      await api.post<PlannerResponse>(
        "/planner",
        payload,
      );

    return data;
  }
}