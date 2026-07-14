import { api } from "@/services/api";

import type {
  PlannerRequest,
  PlannerResponse,
} from "./types";

export class PlannerService {
  static async createPlan(
    payload: PlannerRequest,
  ): Promise<PlannerResponse> {

    const response =
      await api.post<PlannerResponse>(
        "/planner",
        payload,
      );


    console.log(
      "RAW PLANNER API RESPONSE",
      response.data
    );


    return response.data;
  }
}